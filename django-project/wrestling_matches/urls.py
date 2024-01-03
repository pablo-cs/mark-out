from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    # Define your API endpoints here
    path("wrestler/", views.wrestler_view, name="wrestler_view"),
    path("search_wrestler/", views.search_wrestler, name="search_wrestler"),
    path("match/", views.match_view, name="match_view"),
    path("search_match/", views.search_match, name="search_match"),
    path("promotion/", views.promotion_view, name="promotion_view"),
    path("search_promotion/", views.search_promotion, name="search_promotion"),
    path("venue/", views.venue_view, name="venue_view"),
    path("search_venue/", views.search_venue, name="search_venue"),
    path("tag_team/", views.tag_team_view, name="tag_team_view"),
    path("search_tag_team/", views.search_tag_team, name="search_tag_team"),
    path("title/", views.title_view, name="title_view"),
    path("search_title/", views.search_title, name="search_title"),
    path("event/", views.event_view, name="event_view"),
    path("search_event/", views.search_event, name="search_event"),
    path("wrestler_matches/", views.wrestler_matches, name="wrestler_matches"),
    path("event_matches/", views.event_matches, name="event_matches"),
    path("tag_team_matches/", views.tag_team_matches, name="tag_team_matches"),
    path("title_matches/", views.title_matches, name="title_matches"),
    path("venue_events/", views.venue_events, name="venue_events"),
    path("promotion_events/", views.promotion_events, name="promotion_events"),
]
