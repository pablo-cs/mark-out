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
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


class WrestlingMatchesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wrestling_matches"


# Import necessary libraries
import requests
from bs4 import BeautifulSoup


def promotion_scrape():
    current_date = 0
    current_promotion = ""
    current_card_name = ""
    promotion_add = Promotion(name=current_promotion)
    venue_scrape(current_card_name, current_date, promotion_add)
    return


def venue_scrape(current_card_name, current_date, promotion_add):
    current_venue = ""
    current_location = ""
    venue_add = Venue(name=current_venue, location=current_location)
    event_add = Event(
        name=current_card_name,
        venue=venue_add,
        promotion=promotion_add,
        date=current_date,
    )

    return


def match_scrape(event_add):
    current_length = 0
    current_stipulation = ""
    current_title = ""
    match_add = Match(
        event=event_add,
        length=current_length,
        stipulation=current_stipulation,
        title=current_title,
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
