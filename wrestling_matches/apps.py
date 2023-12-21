from django.apps import AppConfig
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
start_url = "http://www.profightdb.com/cards/pg1-no.html/"
response = requests.get(start_url)
soup = BeautifulSoup(response.content, "html.parser")


class WrestlingMatchesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wrestling_matches"


def start_scrape():
    rows = soup.find_all("tr", class_="gray")
    for row in rows:
        columns = row.find_all("td")
        curr_date = columns[0].find("a").get_text()
        curr_promotion = columns[1].find("a").get_text()
        promotion_add = Promotion(name=curr_promotion)
        card_url = base_url + columns[2].find("a")["href"]
        venue_scrape(card_url, curr_date, promotion_add)


def venue_scrape(card_url, curr_date, promotion_add):
    card_response = requests.get(card_url)
    card_soup = BeautifulSoup(card_response.content, "html.parser")
    venue_elem = card_soup.find_all(
        "a", href=lambda href: href and href.startswith("/locations")
    )
    curr_venue = venue_elem[0].get_text()
    curr_location = venue_elem[1].get_text() + ", " + venue_elem[2].get_text()
    curr_card_name = (
        card_soup.find("div", class_="right-content").find("h1").get_text().strip()
    )
    venue_add = Venue(name=curr_venue, location=curr_location)
    event_add = Event(
        name=curr_card_name,
        venue=venue_add,
        promotion=promotion_add,
        date=curr_date,
    )

    return


def match_scrape(event_add, card_soup):
    table = card_soup.find("div", class_="table-wrapper")
    table_body = table.find("table")
    rows = table_body.find_all("tr")[1:]
    for row in rows:
        columns = row.find_all("td")
        curr_result = columns[2].get_text()
        curr_length = columns[4].get_text()
        curr_stipulation = columns[5].get_text()
        curr_title = columns[6].get_text()
        match_add = Match(
            event=event_add,
            length=curr_length,
            stipulation=curr_stipulation,
            title=curr_title,
        )


def participant_scrape(match_add):
    left_tokens = ""
    right_tokens = ""
    has_a_winner = False
    token_scrape(has_a_winner, left_tokens, match_add)
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
                    wrestler_add = Wrestler(site_id=current_site_id, name=current_name)
                current_wrestler = ""  # Replace with wrestler retrieved by site id
                if True:  # replace with if ring name exists already
                    ring_name_add = RingName(
                        name=current_ring_name, wrestler=current_wrestler
                    )
                current_ring_model = ""  # Retrieve ring name model
                match_participant_add = MatchParticipant(
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
                wrestler_add = Wrestler(site_id=current_site_id, name=current_name)
            current_wrestler = ""  # Replace with wrestler retrieved by site id
            if True:  # replace with if ring name exists already
                ring_name_add = RingName(
                    name=current_ring_name, wrestler=current_wrestler
                )
            current_ring_model = ""  # Retrieve ring name model
            match_participant_add = MatchParticipant(
                ring_name=current_ring_model,
                match=match_add,
                is_tag_team=False,
                winner=winner,
            )
