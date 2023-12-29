from django.contrib import admin
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

# Register your models here.

admin.site.register(Wrestler)
admin.site.register(Match)
admin.site.register(MatchParticipant)
admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(Promotion)
admin.site.register(TagTeam)
admin.site.register(RingName)
admin.site.register(Title)
