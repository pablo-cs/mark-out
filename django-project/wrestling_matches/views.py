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

from rest_framework import serializers


class WrestlerSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()
    teams = serializers.SerializerMethodField()

    class Meta:
        model = Wrestler
        fields = "__all__"

    def get_matches(self, obj):
        matches_participated = MatchParticipant.objects.filter(ring_name__wrestler=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )

        class WrestlerMatchSerializer(serializers.ModelSerializer):
            class Meta:
                model = Match
                fields = ("id", "name", "event")

        serializer = WrestlerMatchSerializer(matches, many=True)
        return serializer.data

    def get_teams(self, obj):
        teams = TagTeam.objects.filter(wrestlers=obj)

        class WrestlerTagTeamSerializer(serializers.ModelSerializer):
            class Meta:
                model = TagTeam
                fields = ("id", "name")

        serializer = WrestlerTagTeamSerializer(teams, many=True)
        return serializer.data


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

        class MatchEventSerializer(serializers.ModelSerializer):
            class Meta:
                model = Event
                fields = ("site_id", "name")

        serializer = MatchEventSerializer(event)
        return serializer.data


class VenueSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Venue
        fields = "__all__"

    def get_events(self, obj):
        events = Event.objects.filter(venue=obj)
        serializer = EventSerializer(events, many=True)
        return serializer.data


class EventSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_matches(self, obj):
        matches = Match.objects.filter(event=obj)
        serializer = MatchSerializer(matches, many=True)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = "__all__"

    def get_matches(self, obj):
        matches = obj.matches.all()  # Retrieve all matches related to this title
        serializer = MatchSerializer(matches, many=True)
        return serializer.data


class TagTeamSerializer(serializers.ModelSerializer):
    matches = serializers.SerializerMethodField()
    wrestlers = serializers.SerializerMethodField()

    class Meta:
        model = TagTeam
        fields = "__all__"

    def get_matches(self, obj):
        matches_participated = MatchParticipant.objects.filter(tag_team=obj)
        matches = Match.objects.filter(
            id__in=matches_participated.values_list("match_id", flat=True)
        )
        serializer = MatchSerializer(matches, many=True)
        return serializer.data

    def get_wrestlers(self, obj):
        wrestlers = obj.wrestlers.all()  # Retrieve all matches related to this title

        class TagTeamWrestlerSerializer(serializers.ModelSerializer):
            class Meta:
                model = Wrestler
                fields = ["site_id", "name", "img_src"]

        serializer = TagTeamWrestlerSerializer(wrestlers, many=True)
        return serializer.data


class PromotionSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = "__all__"

    def get_events(self, obj):
        events = Event.objects.filter(promotion=obj)
        serializer = EventSerializer(events, many=True)
        return serializer.data


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


def search_by_query(model, query, **kwargs):
    if query:
        results = model.objects.filter(Q(**kwargs))
        return list(results.values())
    else:
        return []


def wrestler_view(wrestler_id):
    try:
        wrestler = Wrestler.objects.get(site_id=wrestler_id)
        serializer = WrestlerSerializer(wrestler)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Wrestler not found"}, status=404)


def search_wrestler(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(RingName, query, name__icontains=query), safe=False
    )


def match_view(match_id):
    try:
        match = Match.objects.get(id=match_id)
        serializer = MatchSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Match not found"}, status=404)


def search_match(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Match, query, name__icontains=query),
        safe=False,
    )


def promotion_view(promotion_id):
    try:
        match = Promotion.objects.get(id=promotion_id)
        serializer = PromotionSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Promotion not found"}, status=404)


def search_promotion(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Promotion, query, name__icontains=query), safe=False
    )


def venue_view(venue_id):
    try:
        match = Venue.objects.get(id=venue_id)
        serializer = VenueSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Venue not found"}, status=404)


def search_venue(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Venue, query, name__icontains=query, location__icontains=query),
        safe=False,
    )


def tag_team_view(tag_team_id):
    try:
        match = TagTeam.objects.get(id=tag_team_id)
        serializer = TagTeamSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Tag Team not found"}, status=404)


def search_tag_team(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(TagTeam, query, name__icontains=query),
        safe=False,
    )


def title_view(title_id):
    try:
        title = Title.objects.get(id=title_id)
        serializer = TitleSerializer(title)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Title not found"}, status=404)


def search_title(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Title, query, name__icontains=query),
        safe=False,
    )


def event_view(event_id):
    try:
        match = Event.objects.get(site_id=event_id)
        serializer = EventSerializer(match)
        return JsonResponse(serializer.data, safe=False)
    except Wrestler.DoesNotExist:
        return JsonResponse({"error": "Event not found"}, status=404)


def search_event(request):
    query = request.GET.get("query")
    return JsonResponse(
        search_by_query(Event, query, name__icontains=query),
        safe=False,
    )
