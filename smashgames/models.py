from django.db import models
from smashdata.models import Character, GameInfo
from smashtube.util import nontrivial as n, str_or_else as s

class Player(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    mains = models.ManyToManyField(Character)

    def __unicode__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(blank=False, null=False, max_length=200)

    def __unicode__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)

    def __unicode__(self):
        return self.name

class Set(models.Model):
    game = models.ForeignKey(GameInfo, blank=False, null=False)
    tournament = models.ForeignKey(Tournament, blank=True, null=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    description = models.CharField(blank=True, null=False, max_length=50)
    index = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return ", ".join(n(["Set %d" % self.index, s(self.section), s(self.tournament)]))

class Match(models.Model):
    index = models.IntegerField(blank=True, null=False, default=1)
    set = models.ForeignKey(Set, blank=True, null=True)
    players = models.ManyToManyField(Player, through='PlayerSession')
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
    match = models.ForeignKey(Match)
    character = models.ForeignKey(Character)
    team = models.CharField(max_length=1, choices=TEAMS, blank=True, null=False)
    index = models.IntegerField(blank=False, null=False, default=1)