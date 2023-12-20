from django.apps import AppConfig
from bs4 import BeautifulSoup
import requests
from models import (
    Wrestler,
    Match,
    MatchParticipant,
    Venue,
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
