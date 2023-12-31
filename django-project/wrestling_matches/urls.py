from django.urls import path
from . import views

urlpatterns = [
    # Define your API endpoints here
    path("wrestler/<str:wrestler_id>/", views.wrestler_view, name="wrestler_view"),
    path("search_wrestler/", views.search_wrestler, name="search_wrestler"),
    path("match/<int:match_id>/", views.match_view, name="match_view"),
    path("search_match/", views.search_match, name="search_match"),
    path("promotion/<int:promotion_id>/", views.promotion_view, name="promotion_view"),
    path("search_promotion/", views.search_promotion, name="search_promotion"),
    path("venue/<int:venue_id>/", views.venue_view, name="venue_view"),
    path("search_venue/", views.search_venue, name="search_venue"),
    path("tag_team/<int:tag_team_id>/", views.tag_team_view, name="tag_team_view"),
    path("search_tag_team/", views.search_tag_team, name="search_tag_team"),
    path("title/<int:title_id>/", views.title_view, name="title_view"),
    path("search_title/", views.search_title, name="search_title"),
    path("event/<str:event_id>/", views.event_view, name="event_view"),
    path("search_event/", views.search_event, name="search_event"),
    path(
        "wrestler_matches/<str:wrestler_id>/",
        views.wrestler_matches,
        name="wrestler_matches",
    ),
]
