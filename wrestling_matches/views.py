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
    try:
        models = model.objects.get(id=id).values()
        return list(models)
    except model.DoesNotExist:
        return []


def wrestler_view(wrestler_id):
    return JsonResponse(search_by_id(Wrestler, wrestler_id), safe=True)


def search_wrestler(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=True
    )


def match_view(match_id):
    return JsonResponse(search_by_id(Match, match_id), safe=True)


def search_match(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(
            Match, query, matchparticipant__ring_name__wrestler__name__icontains=query
        ),
        safe=True,
    )


def promotion_view(promotion_id):
    return JsonResponse(search_by_id(Promotion, promotion_id), safe=True)


def search_promotion(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=True
    )


def venue_view(venue_id):
    return JsonResponse(search_by_id(Venue, venue_id), safe=True)


def search_venue(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=True,
    )


def tag_team_view(tag_team_id):
    return JsonResponse(search_by_id(TagTeam, tag_team_id), safe=True)


def search_tag_team(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=True,
    )


def title_view(title_id):
    return JsonResponse(search_by_id(Title, title_id), safe=True)


def search_title(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=True,
    )
