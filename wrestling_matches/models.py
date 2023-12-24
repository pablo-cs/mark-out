from django.db import models
from datetime import timedelta
from datetime import date

# Create your models here.


class Promotion(models.Model):
    name = models.CharField(max_length=100)


class Venue(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)


class Event(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)


class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    duration = models.DurationField(default=timedelta(days=0), null=True, blank=True)
    stipulation = models.CharField(max_length=50, null=True, blank=True)
    title = models.CharField(max_length=100)


class TagTeam(models.Model):
    name = models.CharField(max_length=100)
    wrestlers = models.ManyToManyField("Wrestler", related_name="tag_teams")


class Wrestler(models.Model):
    site_id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)


class RingName(models.Model):
    name = models.CharField(max_length=100)
    wrestler = models.ForeignKey(Wrestler, on_delete=models.CASCADE)


class MatchParticipant(models.Model):
    ring_name = models.ForeignKey(RingName, on_delete=models.CASCADE)
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    is_tag_team = models.BooleanField(default=False)
    tag_team = models.ForeignKey(TagTeam, on_delete=models.CASCADE, null=True)
    winner = models.BooleanField(default=False)
