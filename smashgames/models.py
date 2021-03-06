from django.db import models
from smashconstants.models import Character, GameTitle, Stage
from smashtube.util import nontrivial as n, str_or_else as s
 
class Player(models.Model):
    handle = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(blank=True, null=False, default='', max_length=50)
    last_name = models.CharField(blank=True, null=False, default='', max_length=50)
    mains = models.ManyToManyField(Character)

    def __unicode__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(unique=True, max_length=200)
    date = models.DateField(blank=True, null=True)
    location = models.CharField(blank=True, null=False, max_length=200)
    def __unicode__(self):
        return self.name

class Set(models.Model):
    tournament = models.ForeignKey(Tournament, blank=True, null=True)
    description = models.CharField(blank=True, null=False, max_length=50)
    game_title = models.ForeignKey(GameTitle, blank=False, null=False)
    index = models.IntegerField(blank=False, null=False, default=1)

    def __unicode__(self):
        return ", ".join(n(["Set %d" % self.index, s(self.description), s(self.tournament)]))

class Match(models.Model):
    set = models.ForeignKey(Set, blank=True, null=False, related_name='matches')
    index = models.IntegerField(blank=True, null=False, default=1)
    start = models.CharField(blank=True, null=True, max_length=20)
    end = models.CharField(blank=True, null=True, max_length=20)
    stage = models.ForeignKey(Stage, blank=True, null=True)
    players = models.ManyToManyField(Player, through='PlayerSession')
    video_url = models.URLField(blank=False, null=False)
    
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
    match = models.ForeignKey(Match, related_name='player_sessions')
    character = models.ForeignKey(Character)
    team = models.CharField(max_length=1, choices=TEAMS, blank=True, null=False)
    index = models.IntegerField(blank=False, null=False, default=1)