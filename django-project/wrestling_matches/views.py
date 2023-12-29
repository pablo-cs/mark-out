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
        model_inst = None
        model_val = None
        if model == Wrestler:
            model_inst = model.objects.get(site_id=id)
            model_val = model.objects.filter(site_id=id)
        else:
            model_inst = model.objects.get(id=id)
            model_val = model.objects.filter(id=id)

        model_info = list(model_val.values())
        if isinstance(model_inst, Wrestler):
            match_participants = MatchParticipant.objects.filter(
                ring_name__wrestler_id=id
            ).values("match__id")
            matches = Match.objects.filter(id__in=match_participants).values()
            model_info += list(matches)
        elif isinstance(model_inst, Venue):
            events = Event.objects.filter(venue_id=id).values()
            model_info += list(events)
        elif isinstance(model_inst, Event):
            matches = Match.objects.filter(event_id=id).values()
            model_info += list(matches)
        elif isinstance(model_inst, Promotion):
            events = Event.objects.filter(promotion_id=id).values()
            model_info += list(events)
        elif isinstance(model_inst, Title):
            title = Title.objects.get(id=id)
            matches = title.matches.all().values()
            model_info += list(matches)
        elif isinstance(model_inst, TagTeam):
            match_participants = MatchParticipant.objects.filter(tag_team_id=id).values(
                "match__id"
            )
            matches = Match.objects.filter(id__in=match_participants).values()
            model_info += list(matches)
        return model_info
    except model.DoesNotExist:
        return []


def wrestler_view(wrestler_id):
    return JsonResponse(search_by_id(Wrestler, wrestler_id), safe=False)


def search_wrestler(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=False
    )


def match_view(match_id):
    return JsonResponse(search_by_id(Match, match_id), safe=False)


def search_match(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Match, query, name__icontains=query),
        safe=False,
    )


def promotion_view(promotion_id):
    return JsonResponse(search_by_id(Promotion, promotion_id), safe=False)


def search_promotion(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=False
    )


def venue_view(venue_id):
    return JsonResponse(search_by_id(Venue, venue_id), safe=False)


def search_venue(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=False,
    )


def tag_team_view(tag_team_id):
    return JsonResponse(search_by_id(TagTeam, tag_team_id), safe=False)


def search_tag_team(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=False,
    )


def title_view(title_id):
    return JsonResponse(search_by_id(Title, title_id), safe=False)


def search_title(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=False,
    )


def event_view(event_id):
    return JsonResponse(search_by_id(Event, event_id), safe=False)


def search_event(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Event, query, name__icontains=query),
        safe=False,
    )
