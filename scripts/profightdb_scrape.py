from bs4 import BeautifulSoup
import requests
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
page_url = "http://www.profightdb.com/cards/pg1-no.html/"
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

            # Get the date, promotion, and url for the card
            curr_date = columns[0].find("a").get_text()
            curr_promotion = columns[1].find("a").get_text()
            card_url = base_url + columns[2].find("a")["href"]

            # Create Promotion object from promotion name
            promotion_add = Promotion.objects.create(name=curr_promotion)

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

        left_tokens = columns[0].get_text()
        # Result is True if is == def, otherwise False (draw)
        curr_result = columns[1].get_text()[:3].lower() == "def"

        right_tokens = columns[2].get_text()
        # Get duration, stipulation, and title
        curr_length = columns[3].get_text()
        curr_stipulation = columns[4].get_text()
        curr_title = columns[5].get_text()

        # Create Match object from Event, length, stipulation, and title
        match_add = Match.objects.create(
            event=event_add,
            length=curr_length,
            stipulation=curr_stipulation,
            title=curr_title,
        )

        # Scrape participants

        token_scrape(curr_result, left_tokens, match_add)
        token_scrape(False, right_tokens, match_add)


def token_scrape(winner, tokens, match_add):
    for token in tokens:
        if token.find("&") != -1:
            tag_tokens = ""
            current_team_name = ""
            tag_team_add = TagTeam(name=current_team_name)
            for current_ring_name in tag_tokens:
                current_site_id = ""
                if True:  # Replace with current site id is found in DB
                    current_name = ""
                    wrestler_add = Wrestler.objects.create(
                        site_id=current_site_id, name=current_name
                    )
                current_wrestler = ""  # Replace with wrestler retrieved by site id
                if True:  # replace with if ring name exists already
                    ring_name_add = RingName.objects.create(
                        name=current_ring_name, wrestler=current_wrestler
                    )
                current_ring_model = ""  # Retrieve ring name model
                match_participant_add = MatchParticipant.objects.create(
                    ring_name=current_ring_model,
                    match=match_add,
                    is_tag_team=True,
                    tag_team=tag_team_add,
                    winner=winner,
                )
        else:
            current_ring_name = ""
            current_site_id = ""
            if True:  # Replace with current site id is found in DB
                current_name = ""
                wrestler_add = Wrestler.objects.create(
                    site_id=current_site_id, name=current_name
                )
            current_wrestler = ""  # Replace with wrestler retrieved by site id
            if True:  # replace with if ring name exists already
                ring_name_add = RingName.objects.create(
                    name=current_ring_name, wrestler=current_wrestler
                )
            current_ring_model = ""  # Retrieve ring name model
            match_participant_add = MatchParticipant.objects.create(
                ring_name=current_ring_model,
                match=match_add,
                is_tag_team=False,
                winner=winner,
            )
