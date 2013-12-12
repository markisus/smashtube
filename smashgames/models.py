from django.db import models
from smashconstants.models import Character, GameTitle
from smashtube.util import nontrivial as n, str_or_else as s

class Player(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    mains = models.ManyToManyField(Character)

    def __unicode__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(unique=True, max_length=200)

    def __unicode__(self):
        return self.name

class Set(models.Model):
    tournament = models.ForeignKey(Tournament, blank=True, null=True)
    description = models.CharField(blank=True, null=False, max_length=50)
    players = models.ManyToManyField(Player, through='PlayerSession')
    index = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return ", ".join(n(["Set %d" % self.index, s(self.description), s(self.tournament)]))

class Match(models.Model):
    game_title = models.ForeignKey(GameTitle, blank=False, null=False)
    set = models.ForeignKey(Set, blank=True, null=True)
    index = models.IntegerField(blank=True, null=False, default=1)
    video_url = models.URLField(blank=False, null=False)
    start = models.CharField(blank=True, null=False, max_length=20)
    end = models.CharField(blank=True, null=False, max_length=20)

    def __unicode__(self):
        return ", ".join(n(["Match %d" % self.index, s(self.set)]))

class PlayerSession(models.Model):
    TEAMS = (
                ('A', 'A'),
                ('B', 'B'),
                ('C', 'C'),
                ('D', 'D'),
             )
    player = models.ForeignKey(Player)
    set = models.ForeignKey(Set)
    character = models.ForeignKey(Character)
    team = models.CharField(max_length=1, choices=TEAMS, blank=True, null=False)
    index = models.IntegerField(blank=False, null=False, default=1)