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


def search_by_query(model, query, **kwargs):
    if query:
        results = model.objects.filter(Q(**kwargs))
        return list(results.values())
    else:
        return []


def search_by_id(model, id):
    models = model.object.get(id=id).values()
    return models


def wrestler_view(wrestler_id):
    wrestler = Wrestler.objects.get(id=wrestler_id).values()
    return JsonResponse(search_by_id(Wrestler, wrestler_id), safe=True)


def search_wrestler(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=True
    )


def match_view(match_id):
    match = Match.objects.get(id=match_id).values()
    return JsonResponse(list(match), safe=True)


def search_match(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(
            Match, query, matchparticipant__ring_name__wrestler__name__icontains=query
        ),
        safe=True,
    )


def promotion_view(promotion_id):
    promotion = Promotion.objects.get(id=promotion_id).values()
    return JsonResponse(list(promotion), safe=True)


def search_promotion(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=True
    )


def venue_view(venue_id):
    venue = Venue.objects.get(id=venue_id).values()
    return JsonResponse(list(venue), safe=True)


def search_venue(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=True,
    )


def tag_team_view(tag_team_id):
    tag_team = TagTeam.objects.get(id=tag_team_id).values()
    return JsonResponse(list(tag_team), safe=True)


def search_tag_team(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=True,
    )


def title_view(title_id):
    title = TagTeam.objects.get(id=title_id).values()
    return JsonResponse(list(title), safe=True)


def search_title(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=True,
    )
