from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q

from .models import (
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

# Create your views here.


def home_page_view():
    pass


def wrestler_view(wrestler_id):
    wrestler = Wrestler.objects.get(id=wrestler_id).values()
    return JsonResponse(list(wrestler), safe=True)


def search_wrestler(request, wrestler_id):
    query = request
    ring_names = RingName.objects.filter(Q(name__icontains=query))
    return JsonResponse(list(ring_names), safe=True)


def match_view(match_id):
    match = Match.objects.get(id=match_id).values()
    return JsonResponse(list(match), safe=True)


def search_match(request, match_id):
    query = request
    matches = Match.objects.filter(
        Q(matchparticipant__ring_name__wrestler__name__icontains=query)
    )
    return JsonResponse(list(matches), safe=True)


def promotion_view(promotion_id):
    promotion = Promotion.objects.get(id=promotion_id).values()
    return JsonResponse(list(promotion), safe=True)


def search_promotion(request):
    query = request
    promotions = Promotion.objects.filter(Q(name__icontains=query))
    return JsonResponse(list(promotions), safe=True)


def venue_view(venue_id):
    venue = Venue.objects.get(id=venue_id).values()
    return JsonResponse(list(venue), safe=True)


def search_venue(request):
    query = request
    venues = Promotion.objects.filter(
        Q(name__icontains=query) | Q(location__icontains=query)
    )
    return JsonResponse(list(venues), safe=True)


def tag_team_view(tag_team_id):
    tag_team = TagTeam.objects.get(id=tag_team_id).values()
    return JsonResponse(list(tag_team), safe=True)


def search_tag_team(request):
    query = request
    tag_team = TagTeam.objects.filter(Q(name__icontains=query))
    return JsonResponse(list(tag_team), safe=True)


def title_view(title_id):
    title = TagTeam.objects.get(id=title_id).values()
    return JsonResponse(list(title), safe=True)


def search_title(request):
    query = request
    titles = Title.objects.filter(Q(name__icontains=query))
    return JsonResponse(list(titles), safe=True)
