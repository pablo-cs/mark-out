from datetime import timedelta
from bs4 import BeautifulSoup
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
)

base_url = "http://www.profightdb.com/"
page_url = "http://www.profightdb.com/cards/pg1-no.html"
response = requests.get(page_url)
soup = BeautifulSoup(response.content, "html.parser")


def start_scrape():
    pg_count = 1

    # While the page is valid
    while response.status_code == 200:
        # Get all the rows for the page
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

            # Create Promotion object from promotion name or retrieve existing promotion
            promotion_add, created = Promotion.objects.get_or_create(
                name=curr_promotion
            )

            venue_scrape(card_url, curr_date, promotion_add)

        # Increment page count
        pg_count += 1

        # Get new page url, update response object and soup
        page_url = f"http://www.profightdb.com/cards/pg{pg_count}-no.html"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, "html.parser")


def venue_scrape(card_url, curr_date, promotion_add):
    # Get page url for card page and create soup
    card_response = requests.get(card_url)
    card_soup = BeautifulSoup(card_response.content, "html.parser")

    # Get all the location elements and store the venue name and location
    venue_elem = card_soup.find_all(
        "a", href=lambda href: href and href.startswith("/locations")
    )
    curr_venue = venue_elem[0].get_text()
    curr_location = venue_elem[1].get_text() + ", " + venue_elem[2].get_text()

    # Create Venue object from venue name and location
    venue_add = Venue.objects.create(name=curr_venue, location=curr_location)

    # Get the name of the current card
    curr_card_name = (
        card_soup.find("div", class_="right-content").find("h1").get_text().strip()
    )

    # Create Event object from card name, venue, promotion, and date
    event_add = Event.objects.create(
        name=curr_card_name,
        venue=venue_add,
        promotion=promotion_add,
        date=curr_date,
    )

    # Scraping table until have reached the rows
    table = card_soup.find("div", class_="table-wrapper")
    table_body = table.find("table")
    rows = table_body.find_all("tr")[1:]

    # For every row in match table
    for row in rows:
        # Get every column in the row
        columns = row.find_all("td")[1:7]

        # Get wrestlers in winners column
        left_tokens = add_tags(str(columns[0]).split(">, <"))

        # Result is True if is == def, otherwise False (draw)
        curr_result = columns[1].get_text()[:3].lower() == "def"

        # Get wrestlers in losers column
        right_tokens = add_tags(str(columns[2]).split(">, <"))

        # Get duration, stipulation, and title
        duration_str = columns[3].get_text()
        curr_duration = None
        if not duration_str.isspace():
            minutes, seconds = map(int, duration_str.split(":"))
            curr_duration = timedelta(minutes=minutes, seconds=seconds)

        curr_stipulation = columns[4].get_text()
        curr_title = columns[5].get_text()

        # Create Match object from Event, length, stipulation, and title
        match_add = Match.objects.create(
            event=event_add,
            duration=curr_duration,
            stipulation=curr_stipulation,
            title=curr_title,
        )

        # Scrape participants
        token_scrape(curr_result, left_tokens, match_add)
        token_scrape(False, right_tokens, match_add)


def token_scrape(winner, tokens, match_add):
    for token in tokens:
        # Convert text to scrapeable HTML
        token_soup = BeautifulSoup(token, "html.parser")
        if token.find("&") != -1:
            # Split the text into the individual wreslter HTML parts
            tag_tokens = token.split("&")

            # Get the tag team name
            current_team_name = token_soup.get_text()

            tag_team_add = TagTeam.objects.create(name=current_team_name)
            for current_ring_elem in tag_tokens:
                tag_member_soup = BeautifulSoup(current_ring_elem, "html.parser")

                # Extract the site id with regex
                pattern = r"/wrestlers/.*-(\d+).html"
                if tag_member_soup.find("a") is None:
                    continue
                curr_link = tag_member_soup.find("a")["href"]
                match = re.search(pattern, curr_link)
                curr_site_id = match.group(1)
                wrestler_exists = Wrestler.objects.filter(site_id=curr_site_id).exists()

                # Add wrestler if it doesn't exist already in the database
                if not wrestler_exists:
                    # Go to original wrestler's site and extract name
                    new_wrestler_response = requests.get(base_url + curr_link)
                    new_wrestler_soup = BeautifulSoup(
                        new_wrestler_response.content, "html.parser"
                    )
                    curr_wrestler_name = new_wrestler_soup.find("h1").get_text().strip()

                    wrestler_add = Wrestler.objects.create(
                        site_id=curr_site_id, name=curr_wrestler_name
                    )

                # Get the wrestler at the site id
                curr_wrestler = Wrestler.objects.get(site_id=curr_site_id)

                tag_team_add.wrestlers.add(curr_wrestler)

                current_ring_name = tag_member_soup.get_text()

                if current_ring_name.startswith("amp;"):
                    current_ring_name = current_ring_name.replace("amp;", "", 1).strip()

                current_ring_model, created = RingName.objects.get_or_create(
                    name=current_ring_name, wrestler=curr_wrestler
                )

                match_participant_add = MatchParticipant.objects.create(
                    ring_name=current_ring_model,
                    match=match_add,
                    is_tag_team=True,
                    tag_team=tag_team_add,
                    winner=winner,
                )
        else:
            # Extract the site id with regex
            pattern = r"/wrestlers/.*-(\d+).html"
            if token_soup.find("a") is None:
                continue
            curr_link = token_soup.find("a")["href"]
            match = re.search(pattern, curr_link)
            curr_site_id = match.group(1)
            wrestler_exists = Wrestler.objects.filter(site_id=curr_site_id).exists()

            # Add wrestler if it doesn't exist already in the database
            if not wrestler_exists:
                # Go to original wrestler's site and extract name
                new_wrestler_response = requests.get(base_url + curr_link)
                new_wrestler_soup = BeautifulSoup(
                    new_wrestler_response.content, "html.parser"
                )
                curr_wrestler_name = new_wrestler_soup.find("h1").get_text()

                wrestler_add = Wrestler.objects.create(
                    site_id=curr_site_id, name=curr_wrestler_name
                )

            # Get the wrestler at the site id
            curr_wrestler = Wrestler.objects.get(site_id=curr_site_id)

            current_ring_name = token_soup.get_text()

            # Create a RingName object if not found, or get the one found
            current_ring_model, created = RingName.objects.get_or_create(
                name=current_ring_name, wrestler=curr_wrestler
            )

            match_participant_add = MatchParticipant.objects.create(
                ring_name=current_ring_model,
                match=match_add,
                is_tag_team=False,
                winner=winner,
            )


def add_tags(strings):
    modified_strings = []
    for string in strings:
        if not string.startswith("<"):
            string = "<" + string
        if not string.endswith(">"):
            string += ">"
        modified_strings.append(string)
    return modified_strings
