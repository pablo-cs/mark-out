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

from django.core.paginator import Paginator, EmptyPage
import logging

# Create your views here.

from rest_framework import serializers
from django.core.cache import cache


class WrestlerSerializer(serializers.ModelSerializer):
    ring_names = serializers.SerializerMethodField()

    class Meta:
        model = Wrestler
        fields = "__all__"

    def get_matches(self, obj):
        matches_participated = MatchParticipant.objects.filter(ring_name__wrestler=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )

        # serializer = MatchSerializer(matches, many=True)
        return matches

    def get_teams(self, obj):
        teams = TagTeam.objects.filter(wrestlers=obj)
        serializer = SubTagTeamSerializer(teams, many=True)
        return serializer.data

    def get_ring_names(self, obj):
        ring_names = RingName.objects.filter(wrestler=obj).values("id", "name")
        serializer = SubRingNameSerializer(ring_names, many=True)
        return serializer.data


class SubWrestlerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wrestler
        fields = ["site_id", "name", "img_src"]


class MatchSerializer(serializers.ModelSerializer):
    match_participants = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = "__all__"

    def get_match_participants(self, obj):
        match_participants = MatchParticipant.objects.filter(match=obj)

        serializer = MatchParticipantSerializer(match_participants, many=True)
        return serializer.data

    def get_event(self, obj):
        event = obj.event
        serializer = SubEventSerializer(event)
        return serializer.data


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"

    def get_events(self, obj):
        events = Event.objects.filter(venue=obj).values(
            "site_id", "name", "promotion", "date"
        )
        return events


class SubEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTeam
        fields = ["site_id", "name", "promotion", "date"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    def get_matches(self, obj):
        matches = Match.objects.filter(event=obj)
        return matches


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = "__all__"

    def get_matches(self, obj):
        matches = obj.matches.all()  # Retrieve all matches related to this title
        return matches


class TagTeamSerializer(serializers.ModelSerializer):
    wrestlers = serializers.SerializerMethodField()

    class Meta:
        model = TagTeam
        fields = "__all__"

    def get_matches(self, obj):
        matches_participated = MatchParticipant.objects.filter(tag_team=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )
        return matches

    def get_wrestlers(self, obj):
        wrestlers = obj.wrestlers.all().values("site_id", "name", "img_src")
        serializer = SubWrestlerSerializer(wrestlers, many=True)
        return serializer.data


class SubTagTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagTeam
        fields = ("id", "name")


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = "__all__"

    def get_events(self, obj):
        events = Event.objects.filter(venue=obj).values(
            "site_id", "name", "promotion", "date"
        )
        return events


class MatchParticipantSerializer(serializers.ModelSerializer):
    ring_name = serializers.SerializerMethodField()

    class Meta:
        model = MatchParticipant
        fields = "__all__"

    def get_ring_name(self, obj):
        ring_name = obj.ring_name
        serializer = RingNameSerializer(ring_name)
        return serializer.data


class RingNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RingName
        fields = "__all__"


class SubRingNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RingName
        fields = ("id", "name")


def search_by_query(model, query, page_number=1, items_per_page=10, **kwargs):
    if query:
        results = model.objects.filter(Q(**kwargs))
        paginator = Paginator(results, items_per_page)
        try:
            paginated_results = paginator.page(page_number)
            return list(paginated_results.object_list.values())
        except EmptyPage:
            # If page is out of range, return an empty list (you can handle this differently as needed)
            return []
    else:
        return []


def wrestler_view(request, wrestler_id):
    try:
        cache_key = f"wrestler_{wrestler_id}"
        wrestler = cache.get(cache_key)
        if not wrestler:
            wrestler = Wrestler.objects.get(site_id=wrestler_id)
            cache.set(cache_key, wrestler, timeout=3600)  # Cache for 1 hour
        serializer = WrestlerSerializer(wrestler)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Wrestler not found"}, status=404)


def search_wrestler(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=False
    )


def match_view(request, match_id):
    try:
        cache_key = f"match{match_id}"
        match = cache.get(cache_key)
        if not match:
            match = Match.objects.get(id=match_id)
            cache.set(cache_key, match, timeout=3600)
        serializer = MatchSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Match.DoesNotExist:
        return JsonResponse({"error": "Match not found"}, status=404)


def search_match(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Match, query, name__icontains=query),
        safe=False,
    )


def promotion_view(request, promotion_id):
    try:
        cache_key = f"promotion{promotion_id}"
        promotion = cache.get(cache_key)
        if not promotion:
            promotion = Promotion.objects.get(id=promotion_id)
            cache.set(cache_key, promotion, timeout=3600)
        serializer = PromotionSerializer(promotion)
        return JsonResponse(serializer.data, safe=False)
    except Promotion.DoesNotExist:
        return JsonResponse({"error": "Promotion not found"}, status=404)


def search_promotion(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=False
    )


def venue_view(request, venue_id):
    try:
        cache_key = f"venue{venue_id}"
        venue = cache.get(cache_key)
        if not venue:
            venue = Venue.objects.get(id=venue_id)
            cache.set(cache_key, venue, timeout=3600)
        serializer = VenueSerializer(venue)
        return JsonResponse(serializer.data, safe=False)
    except Venue.DoesNotExist:
        return JsonResponse({"error": "Venue not found"}, status=404)


def search_venue(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=False,
    )


def tag_team_view(request, tag_team_id):
    try:
        cache_key = f"tag_team{tag_team_id}"
        tag_team = cache.get(cache_key)
        if not tag_team:
            tag_team = TagTeam.objects.get(id=tag_team_id)
            cache.set(cache_key, tag_team, timeout=3600)
        serializer = TagTeamSerializer(tag_team)
        return JsonResponse(serializer.data, safe=False)
    except TagTeam.DoesNotExist:
        return JsonResponse({"error": "Tag Team not found"}, status=404)


def search_tag_team(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=False,
    )


def title_view(request, title_id):
    try:
        cache_key = f"title{title_id}"
        title = cache.get(cache_key)
        if not title:
            title = Title.objects.get(id=title_id)
            cache.set(cache_key, title, timeout=3600)
        serializer = TitleSerializer(title)
        return JsonResponse(serializer.data, safe=False)
    except Title.DoesNotExist:
        return JsonResponse({"error": "Title not found"}, status=404)


def search_title(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=False,
    )


def event_view(request, event_id):
    try:
        cache_key = f"event{event_id}"
        event = cache.get(cache_key)
        if not event:
            event = Event.objects.get(site_id=event_id)
            cache.set(cache_key, event, timeout=3600)
        serializer = EventSerializer(event)
        return JsonResponse(serializer.data, safe=False)
    except Event.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)


def search_event(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Event, query, name__icontains=query),
        safe=False,
    )


def wrestler_matches(request, wrestler_id):
    return get_info(request, wrestler_id, Wrestler, Match)


def event_matches(request, event_id):
    return get_info(request, event_id, Event, Match)


def tag_team_matches(request, tag_team_id):
    return get_info(request, tag_team_id, TagTeam, Match)


def title_matches(request, title_id):
    return get_info(request, title_id, Title, Match)


def venue_events(request, venue_id):
    return get_info(request, venue_id, Venue, Event)


def promotion_events(request, promotion_id):
    return get_info(request, promotion_id, Promotion, Event)


def get_info(request, id, model, retrieve):
    model_info = {
        Wrestler: ["wrestler", WrestlerSerializer],
        TagTeam: ["tag_team", TagTeamSerializer],
        Event: ["event", EventSerializer],
        Title: ["title", TitleSerializer],
        Venue: ["venue", VenueSerializer],
        Promotion: ["promotion", PromotionSerializer],
    }

    retr_info = {Match: MatchSerializer, Event: EventSerializer}

    model_str = model_info[model][0]
    cache_key = f"{model_str}_{id}"
    model_obj = cache.get(cache_key)

    if not model_obj:
        try:
            if model == Wrestler or model == Event:
                model_obj = model.objects.get(site_id=id)
            else:
                model_obj = model.objects.get(id=id)
            cache.set(cache_key, model_obj, timeout=3600)  # Cache for 1 hour
        except model.DoesNotExist:
            return JsonResponse({"error": f"{model.__name__} not found"}, status=404)

    model_serializer_type = model_info[model][1]
    model_serializer = model_serializer_type(model_obj)

    paginate_info = None
    if retrieve == Match:
        paginate_info = model_serializer.get_matches(model_obj)
    else:
        paginate_info = model_serializer.get_events(model_obj)

    paginated_info = get_paginated_response(paginate_info, retr_info[retrieve], request)

    return JsonResponse({"matches": paginated_info}, safe=False)


def get_paginated_response(queryset, serializer_class, request):
    paginator = Paginator(queryset, per_page=10)  # Adjust per_page as needed
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    serialized_data = serializer_class(page_obj, many=True).data
    return serialized_data
