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
from rest_framework import serializers
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage

# Create your views here.


class WrestlerSerializer(serializers.ModelSerializer):
    """Serializer for Wrestler model."""

    ring_names = serializers.SerializerMethodField()

    class Meta:
        model = Wrestler
        fields = "__all__"

    def get_matches(self, obj):
        """
        Retrieve matches in which the wrestler participated.

        Args:
            obj: Wrestler instance.

        Returns:
            List of matches associated with the wrestler.
        """
        matches_participated = MatchParticipant.objects.filter(ring_name__wrestler=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )

        # serializer = MatchSerializer(matches, many=True)
        return matches

    def get_teams(self, obj):
        """
        Retrieve tag teams the wrestler is a part of.

        Args:
            obj: Wrestler instance.

        Returns:
            Serialized data of tag teams with the wrestler.
        """
        teams = TagTeam.objects.filter(wrestlers=obj)
        serializer = SubTagTeamSerializer(teams, many=True)
        return serializer.data

    def get_ring_names(self, obj):
        """
        Retrieve ring names associated with the wrestler.

        Args:
            obj: Wrestler instance.

        Returns:
            Serialized data of ring names for the wrestler.
        """
        ring_names = RingName.objects.filter(wrestler=obj).values("id", "name")
        serializer = SubRingNameSerializer(ring_names, many=True)
        return serializer.data


class SubWrestlerSerializer(serializers.ModelSerializer):
    """Serializer for subset of Wrestler model."""

    class Meta:
        model = Wrestler
        fields = ["site_id", "name", "img_src"]


class MatchSerializer(serializers.ModelSerializer):
    """Serializer for Match model."""

    match_participants = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = "__all__"

    def get_match_participants(self, obj):
        """
        Retrieve match participants associated with a match.

        Args:
            obj: Match instance.

        Returns:
            Serialized data of match participants.
        """
        match_participants = MatchParticipant.objects.filter(match=obj)

        serializer = MatchParticipantSerializer(match_participants, many=True)
        return serializer.data

    def get_event(self, obj):
        """
        Retrieve event associated with a match.

        Args:
            obj: Match instance.

        Returns:
            Serialized data of the associated event.
        """
        event = obj.event
        serializer = SubEventSerializer(event)
        return serializer.data


class VenueSerializer(serializers.ModelSerializer):
    """Serializer for Venue model."""

    class Meta:
        model = Venue
        fields = "__all__"

    def get_events(self, obj):
        """
        Retrieve events associated with a venue.

        Args:
            obj: Venue instance.

        Returns:
            Serialized data of events related to the venue.
        """
        events = Event.objects.filter(venue=obj).values(
            "site_id", "name", "promotion", "date"
        )
        return events


class SubEventSerializer(serializers.ModelSerializer):
    """Serializer for specific event data."""

    class Meta:
        model = Event
        fields = ["site_id", "name", "promotion", "date"]


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    class Meta:
        model = Event
        fields = "__all__"

    def get_matches(self, obj):
        """
        Retrieve matches associated with an event.

        Args:
            obj: Event instance.

        Returns:
            Matches related to the event serialized in data format.
        """
        matches = Match.objects.filter(event=obj)
        return matches


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title model."""

    class Meta:
        model = Title
        fields = "__all__"

    def get_matches(self, obj):
        """
        Retrieve matches associated with a title.

        Args:
            obj: Title instance.

        Returns:
            Matches related to the title serialized in data format.
        """
        matches = obj.matches.all()  # Retrieve all matches related to this title
        return matches


class TagTeamSerializer(serializers.ModelSerializer):
    """Serializer for TagTeam model."""

    wrestlers = serializers.SerializerMethodField()

    class Meta:
        model = TagTeam
        fields = "__all__"

    def get_matches(self, obj):
        """
        Retrieve matches participated by a tag team.

        Args:
            obj: TagTeam instance.

        Returns:
            Matches participated by the tag team serialized in data format.
        """
        matches_participated = MatchParticipant.objects.filter(tag_team=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )
        return matches

    def get_wrestlers(self, obj):
        """
        Retrieve wrestlers in a tag team.

        Args:
            obj: TagTeam instance.

        Returns:
            Serialized data of wrestlers in the tag team.
        """
        wrestlers = obj.wrestlers.all().values("site_id", "name", "img_src")
        serializer = SubWrestlerSerializer(wrestlers, many=True)
        return serializer.data


class SubTagTeamSerializer(serializers.ModelSerializer):
    """Serializer for Sub TagTeam model."""

    class Meta:
        model = TagTeam
        fields = ("id", "name")


class PromotionSerializer(serializers.ModelSerializer):
    """Serializer for Promotion model."""

    class Meta:
        model = Promotion
        fields = "__all__"

    def get_events(self, obj):
        """
        Retrieve events associated with a promotion.

        Args:
            obj: Promotion instance.

        Returns:
            Serialized data of events related to the promotion.
        """
        events = Event.objects.filter(venue=obj).values(
            "site_id", "name", "promotion", "date"
        )
        return events


class MatchParticipantSerializer(serializers.ModelSerializer):
    """Serializer for MatchParticipant model."""

    ring_name = serializers.SerializerMethodField()

    class Meta:
        model = MatchParticipant
        fields = "__all__"

    def get_ring_name(self, obj):
        """
        Retrieve the ring name of a match participant.

        Args:
            obj: MatchParticipant instance.

        Returns:
            Serialized data of the ring name associated with the match participant.
        """
        ring_name = obj.ring_name
        serializer = RingNameSerializer(ring_name)
        return serializer.data


class RingNameSerializer(serializers.ModelSerializer):
    """Serializer for RingName model."""

    class Meta:
        model = RingName
        fields = "__all__"


class SubRingNameSerializer(serializers.ModelSerializer):
    """Serializer for Sub RingName model."""

    class Meta:
        model = RingName
        fields = ("id", "name")


def search_by_query(model, query, page_number=1, items_per_page=10, **kwargs):
    """
    Perform a search in the database based on query parameters.

    Args:
        model: The model to search within.
        query: The search query.
        page_number: The page number for pagination (default: 1).
        items_per_page: Number of items per page (default: 10).
        **kwargs: Additional filtering parameters.

    Returns:
        A list of paginated search results.
    """
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


def get_cached_object(cache_key, model, id):
    """
    Retrieve an object from cache or database and cache it.

    Args:
        cache_key: The key to use for caching.
        model: The Django model for the object.
        id: ID of the object.

    Returns:
        The cached object or None if not found.
    """
    cached_obj = cache.get(cache_key)
    if not cached_obj:
        try:
            if model == Wrestler or model == Event:
                cached_obj = model.objects.get(site_id=id)
            else:
                cached_obj = model.objects.get(id=id)
            cache.set(cache_key, cached_obj, timeout=3600)  # Cache for 1 hour
        except model.DoesNotExist:
            cached_obj = None
    return cached_obj


def wrestler_view(request):
    """
    Retrieve details of a specific Wrestler.

    Args:
        request: The request object.

    Returns:
        Details of the Wrestler in JSON format.
    """
    wrestler_id = request.GET.get("wrestler_id")
    if wrestler_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_wrestler(request):
    """
    Search for Wrestlers based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Wrestlers in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=False
    )


def match_view(request):
    """
    Retrieve details of a specific Match.

    Args:
        request: The request object.

    Returns:
        Details of the Match in JSON format.
    """

    match_id = request.GET.get("match_id")
    if match_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_match(request):
    """
    Search for Matches based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Matches in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Match, query, name__icontains=query),
        safe=False,
    )


def promotion_view(request):
    """
    Retrieve details of a specific Promotion.

    Args:
        request: The request object.

    Returns:
        Details of the Promotion in JSON format.
    """
    promotion_id = request.GET.get("promotion_id")
    if promotion_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_promotion(request):
    """
    Search for Promotion based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Promotion in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=False
    )


def venue_view(request):
    """
    Retrieve details of a specific Venue.

    Args:
        request: The request object.

    Returns:
        Details of the Venue in JSON format.
    """
    venue_id = request.GET.get("venue_id")
    if venue_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_venue(request):
    """
    Search for Venues based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Venues in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=False,
    )


def tag_team_view(request):
    """
    Retrieve details of a specific TagTeam.

    Args:
        request: The request object.

    Returns:
        Details of the TagTeam in JSON format.
    """
    tag_team_id = request.GET.get("tag_team_id")
    if tag_team_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_tag_team(request):
    """
    Search for TagTeams based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for TagTeams in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=False,
    )


def title_view(request):
    """
    Retrieve details of a specific Title.

    Args:
        request: The request object.

    Returns:
        Details of the Title in JSON format.
    """
    title_id = request.GET.get("title_id")
    if title_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_title(request):
    """
    Search for Titles based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Titles in JSON format.
    """

    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=False,
    )


def event_view(request):
    """
    Retrieve details of a specific Event.

    Args:
        request: The request object.

    Returns:
        Details of the Event in JSON format.
    """
    event_id = request.GET.get("event_id")
    if event_id:
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
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def search_event(request):
    """
    Search for Events based on query parameters.

    Args:
        request: The request object.

    Returns:
        Search results for Events in JSON format.
    """
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Event, query, name__icontains=query),
        safe=False,
    )


def wrestler_matches(request):
    """
    Retrieve matches related to a specific Wrestler.

    Args:
        request: The request object.

    Returns:
        JSON response containing matches associated with the Wrestler.
    """
    wrestler_id = request.GET.get("wrestler_id")
    if wrestler_id:
        return get_info(request, wrestler_id, Wrestler, Match)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def event_matches(request):
    """
    Retrieve matches related to a specific Event.

    Args:
        request: The request object.

    Returns:
        JSON response containing matches associated with the Event.
    """
    event_id = request.GET.get("event_id")
    if event_id:
        return get_info(request, event_id, Event, Match)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def tag_team_matches(request):
    """
    Retrieve matches related to a specific Tag Team.

    Args:
        request: The request object.

    Returns:
        JSON response containing matches associated with the Tag Team.
    """
    tag_team_id = request.GET.get("tag_team_id")
    if tag_team_id:
        return get_info(request, tag_team_id, TagTeam, Match)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def title_matches(request):
    """
    Retrieve matches related to a specific Title.

    Args:
        request: The request object.

    Returns:
        JSON response containing matches associated with the Title.
    """
    title_id = request.GET.get("title_id")
    if title_id:
        return get_info(request, title_id, Title, Match)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def venue_events(request):
    """
    Retrieve events related to a specific Venue.

    Args:
        request: The request object.

    Returns:
        JSON response containing events associated with the Venue.
    """
    venue_id = request.GET.get("venue_id")
    if venue_id:
        return get_info(request, venue_id, Venue, Event)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def promotion_events(request):
    """
    Retrieve events related to a specific Promotion.

    Args:
        request: The request object.

    Returns:
        JSON response containing events associated with the Promotion.
    """
    promotion_id = request.GET.get("promotion_id")
    if promotion_id:
        return get_info(request, promotion_id, Promotion, Event)
    else:
        return JsonResponse({"error": "Invalid Arguments"}, status=404)


def get_info(request, id, model, retrieve):
    """
    Fetch information based on given parameters.

    Args:
        request: The request object.
        id: ID of the item.
        model: The Django model for which information is fetched.
        retrieve: The type of data to retrieve.

    Returns:
        JSON response with the requested information.
    """
    model_info = {
        Wrestler: ["wrestler", WrestlerSerializer],
        TagTeam: ["tag_team", TagTeamSerializer],
        Event: ["event", EventSerializer],
        Title: ["title", TitleSerializer],
        Venue: ["venue", VenueSerializer],
        Promotion: ["promotion", PromotionSerializer],
    }

    retr_info = {
        Match: ["matches", MatchSerializer],
        Event: ["events", EventSerializer],
    }

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
    paginate_str = retr_info[retrieve][0]
    paginate_serializer_type = retr_info[retrieve][1]
    if retrieve == Match:
        paginate_info = model_serializer.get_matches(model_obj)
        paginate_str
    else:
        paginate_info = model_serializer.get_events(model_obj)

    paginated_info = get_paginated_response(
        paginate_info, paginate_serializer_type, request
    )

    return JsonResponse({f"{paginate_str}": paginated_info}, safe=False)


def get_paginated_response(queryset, serializer_class, request):
    """
    Paginate a queryset and serialize the data.

    Args:
        queryset: The queryset to paginate.
        serializer_class: The serializer class to use for serialization.
        request: The request object.

    Returns:
        Serialized data in paginated form.
    """
    paginator = Paginator(queryset, per_page=10)  # Adjust per_page as needed
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    serialized_data = serializer_class(page_obj, many=True).data
    return serialized_data
