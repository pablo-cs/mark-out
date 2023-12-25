from django.db import transaction
from datetime import timedelta
from bs4 import BeautifulSoup
import logging
import re
import requests
from dateutil.parser import parse
from models import (
    Wrestler,
    Match,
    MatchParticipant,
    Venue,
    Event,
    Promotion,
    TagTeam,
    RingName,
    Title,
)

base_url = "http://www.profightdb.com/"
page_url = "http://www.profightdb.com/cards/pg1-no.html"
response = requests.get(page_url)
soup = BeautifulSoup(response.content, "html.parser")
logging.basicConfig(level=logging.INFO)


@transaction.atomic()
def start_scrape():
    """ """
    pg_count = 1

    # While the page is valid
    while response.status_code == 200:
        # Get all the rows for the page
        logging.info(f"Scraping page {pg_count}")

        try:
            rows = soup.find_all("tr", class_="gray")

            # Go through each row
            for row in rows:
                # Get all the columns for the row
                columns = row.find_all("td")

                # Get the date and convert to a Date object
                curr_date = parse(columns[0].find("a").get_text())

                # Get the promotion and url card
                curr_promotion = columns[1].find("a").get_text()
                card_url = base_url + columns[2].find("a")["href"]

                pattern = r"/cards/.*-(\d+).html"
                curr_site_id = re.search(pattern, card_url).group(1)

                event_exists = Event.objects.filter(site_id=curr_site_id).exists()
                if event_exists:
                    continue
                # Create Promotion object from promotion name or retrieve existing promotion
                promotion_add, created = Promotion.objects.get_or_create(
                    name=curr_promotion
                )
                logging.info(f"Scraping promotion: {curr_promotion}")

                card_response = requests.get(card_url)
                card_soup = BeautifulSoup(card_response.content, "html.parser")

                venue_add = venue_scrape(card_soup)
                event_add = event_scrape(
                    card_soup, curr_site_id, venue_add, promotion_add, curr_date
                )
                card_scrape(card_soup, event_add)
            # Increment page count
            pg_count += 1

            # Get new page url, update response object and soup
            page_url = f"http://www.profightdb.com/cards/pg{pg_count}-no.html"
            response = requests.get(page_url)
            soup = BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            logging.error(f"Error occurred while scraping page {pg_count}: {e}")


@transaction.atomic()
def venue_scrape(card_soup):
    """
    Scrapes the venue information from a given card and returns
    an Venue object
    """
    try:
        # Get all the location elements and store the venue name and location
        venue_elem = card_soup.find_all(
            "a", href=lambda href: href and href.startswith("/locations")
        )
        curr_venue = venue_elem[0].get_text()
        curr_location = venue_elem[1].get_text() + ", " + venue_elem[2].get_text()

        # Create Venue object from venue name and location
        logging.info(f"Scraping Venue: {curr_venue} , {curr_location}")

        return Venue.objects.create(name=curr_venue, location=curr_location)

    except Exception as e:
        logging.error(f"Error occurred while scraping venue: {e}")


@transaction.atomic()
def event_scrape(card_soup, site_id, venue_add, promotion_add, curr_date):
    """
    Scrapes the event information from a given card and returns
    an Event object
    """
    try:
        # Get the name of the current card
        curr_event_name = (
            card_soup.find("div", class_="right-content").find("h1").get_text().strip()
        )

        logging.info(f"Scraping Event: {curr_event_name}")

        # Create Event object from card name, venue, promotion, and date
        return Event.objects.create(
            site_id=site_id,
            name=curr_event_name,
            venue=venue_add,
            promotion=promotion_add,
            date=curr_date,
        )
    except Exception as e:
        logging.error(f"Error occurred while scraping event: {card_soup}, {e}")


@transaction.atomic()
def card_scrape(card_soup, event_add):
    """
    Scrapes the matches from a card
    """
    try:
        # Scraping table until have reached the rows
        table = card_soup.find("div", class_="table-wrapper")
        table_body = table.find("table")
        rows = table_body.find_all("tr")[1:]

        for row in rows:
            # Get every column in the row
            columns = row.find_all("td")[1:7]

            # Get wrestlers in winners column
            left_tokens = add_tags(str(columns[0]).split(">, <"))

            logging.info(f"Scraping Winner Column: {left_tokens}")

            # Result is True if is == def, otherwise False (draw)
            curr_result = columns[1].get_text()[:3].lower() == "def"
            logging.info(f"Scraping Result: {curr_result}")

            # Get wrestlers in losers column
            right_tokens = add_tags(str(columns[2]).split(">, <"))
            logging.info(f"Scraping Loser Column: {right_tokens}")

            # Get duration, stipulation, and title
            duration_str = columns[3].get_text()
            curr_duration = None
            if not duration_str.isspace():
                minutes, seconds = map(int, duration_str.split(":"))
                curr_duration = timedelta(minutes=minutes, seconds=seconds)
                logging.info(f"Scraping Match Duration: {curr_duration}")

            curr_stipulation = columns[4].get_text()
            logging.info(f"Scraping Match Stipulation: {curr_stipulation}")

            curr_title_text = columns[5].get_text(separator="\n", strip=True)

            # Split the text based on <br> tags and create a list
            curr_titles = [
                title.strip() for title in curr_title_text.split("\n") if title.strip()
            ]

            logging.info(f"Scraping Match Title(s): {curr_titles}")

            # Create Match object from Event, length, stipulation, and title
            match_add = Match.objects.create(
                event=event_add,
                duration=curr_duration,
                stipulation=curr_stipulation,
            )

            for title in curr_titles:
                if title != "(Title Change)":
                    # Create or get the Title object
                    title_obj, created = Title.objects.get_or_create(name=title)

                    # Add match_add to the many-to-many field only if it's not a "(Title Change)"
                    title_obj.match.add(match_add)

            # Scrape participants
            logging.info("Scraping Left Columm Participants")
            token_scrape(curr_result, left_tokens, match_add)

            logging.info("Scraping Right Columm Participants")
            token_scrape(False, right_tokens, match_add)
    except Exception as e:
        logging.error(f"Error occurred while scraping card for: {event_add.name}, {e}")


@transaction.atomic()
def token_scrape(winner, tokens, match_add):
    """
    Scrapes participant information, adding new wrestlers and ring names
    as they appear, and adding the match participant
    """
    try:
        for token in tokens:
            # Convert text to scrapeable HTML
            token_soup = BeautifulSoup(token, "html.parser")
            if token.find("&") != -1:
                # Split the text into the individual wreslter HTML parts
                tag_tokens = token.split("&")

                # Get the tag team name
                current_team_name = token_soup.get_text()
                logging.info(f"Scraping Tag Team: {current_team_name}")

                tag_team_add = TagTeam.objects.create(name=current_team_name)
                for current_ring_elem in tag_tokens:
                    # Convert text to scrapeable HTML
                    tag_member_soup = BeautifulSoup(current_ring_elem, "html.parser")

                    logging.info(
                        f"Scraping Tag Team Member: {tag_member_soup.get_text()}"
                    )
                    # Scrape individual participant
                    participant_scrape(
                        tag_member_soup, winner, match_add, True, tag_team_add
                    )

            else:
                # Scrape individual participant
                logging.info(f"Scraping Singles Wreslter: {token_soup.get_text()}")
                participant_scrape(token_soup, False, match_add)
    except Exception as e:
        logging.error(f"Error occurred while scraping tokens: {tokens}, {e}")


@transaction.atomic()
def participant_scrape(
    participant_soup,
    winner,
    match_add,
    is_tag_member=False,
    tag_team_add=None,
    champ=False,
):
    """
    Scrapes individual match participant information and creates objects for all of tem
    """
    try:
        # Extract the site id with regex
        pattern = r"/wrestlers/.*-(\d+).html"
        if participant_soup.find("a") is None:
            return

        curr_link = participant_soup.find("a")["href"]
        logging.info(f"Scraping Wrestler Link: {curr_link}")

        match = re.search(pattern, curr_link)
        curr_site_id = match.group(1)
        logging.info(f"Scraping Wrestler Site ID: {curr_site_id}")

        wrestler_exists = Wrestler.objects.filter(site_id=curr_site_id).exists()

        # Add wrestler if it doesn't exist already in the database
        if not wrestler_exists:
            # Go to original wrestler's site and extract name
            new_wrestler_response = requests.get(base_url + curr_link)
            new_wrestler_soup = BeautifulSoup(
                new_wrestler_response.content, "html.parser"
            )
            curr_wrestler_name = new_wrestler_soup.find("h1").get_text()
            logging.info(f"Scraping New Wreslter: {curr_wrestler_name}")

            wrestler_add = Wrestler.objects.create(
                site_id=curr_site_id, name=curr_wrestler_name
            )

        # Get the wrestler at the site id
        curr_wrestler = Wrestler.objects.get(site_id=curr_site_id)

        # Adds to TagTeam object's wrestlers list if needed
        if is_tag_member and tag_team_add is not None:
            tag_team_add.wrestlers.add(curr_wrestler)

        current_ring_name = participant_soup.get_text()

        if current_ring_name.startswith("amp;"):
            current_ring_name = current_ring_name.replace("amp;", "", 1).strip()

        if current_ring_name.endswith("(c)"):
            current_ring_name = current_ring_name.replace("(c)", "", 1).strip()
            champ = True

        # Create a RingName object if not found, or get the one found
        current_ring_model, created = RingName.objects.get_or_create(
            name=current_ring_name, wrestler=curr_wrestler
        )

        match_participant_add = MatchParticipant.objects.create(
            ring_name=current_ring_model,
            match=match_add,
            is_tag_team=is_tag_member,
            tag_team=tag_team_add,
            winner=winner,
            champion=champ,
        )
    except Exception as e:
        logging.error(
            f"Error occurred while scraping participant {participant_soup}: {e}"
        )


def add_tags(strings):
    """
    Correct the result of splitting HTML by commas and readds arrows
    to strings
    """
    modified_strings = []
    for string in strings:
        if not string.startswith("<"):
            string = "<" + string
        if not string.endswith(">"):
            string += ">"
        modified_strings.append(string)
    return modified_strings
