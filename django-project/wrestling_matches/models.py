from django.db import models
from datetime import timedelta
from datetime import date

# Create your models here.


class Promotion(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}, {self.location}"


class Event(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=500)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.name} ({self.site_id}) at {self.venue.name} - {self.date}"


class Match(models.Model):
    name = models.CharField(max_length=4000, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    duration = models.DurationField(default=timedelta(days=0), null=True, blank=True)
    stipulation = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name} at Event: {self.event.name}"


class Title(models.Model):
    name = models.CharField(max_length=500)
    matches = models.ManyToManyField("Match", related_name="titles")

    def __str__(self):
        return self.name


class TagTeam(models.Model):
    name = models.CharField(max_length=1000)
    wrestlers = models.ManyToManyField("Wrestler", related_name="tag_teams")

    def __str__(self):
        return self.name


class Wrestler(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    img_src = models.CharField(default=None, max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class RingName(models.Model):
    name = models.CharField(max_length=100)
    wrestler = models.ForeignKey(Wrestler, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.wrestler.name})"


class MatchParticipant(models.Model):
    ring_name = models.ForeignKey(RingName, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    is_tag_team = models.BooleanField(default=False)
    tag_team = models.ForeignKey(TagTeam, on_delete=models.CASCADE, null=True)
    winner = models.BooleanField(default=False)
    champion = models.BooleanField(default=False)

    def __str__(self):
        return f"Participant: {self.ring_name.name} in Match: {self.match.event.name}"
