# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from models import Tournament, Set, Match, VideoURL, Player, PlayerSession
from forms import TournamentForm

class TournamentResource(ModelResource):
    class Meta:
        queryset = Tournament.objects.all()
        resource_name = 'tournament'
        authorization = Authorization()
        validation = FormValidation(form_class=TournamentForm)
        filtering = {'name': ['icontains']}

class SetResource(ModelResource):
    class Meta:
        queryset = Set.objects.all()
        resource_name = 'set'
        authorization = Authorization()
        filtering = {'name': ['icontains']}

class MatchResource(ModelResource):
    class Meta:
        queryset = Match.objects.all()
        resource_name = 'match'
        authorization = Authorization()
        filtering = {'name': ['icontains']}

class VideoURLResource(ModelResource):
    class Meta:
        queryset = VideoURL.objects.all()
        resource_name = 'video-url'
        authorization = Authorization()
        filtering = {'name': ['icontains']}

class PlayerResource(ModelResource):
    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'
        authorization = Authorization()
        filtering = {'name': ['icontains']}

class PlayerSessionResource(ModelResource):
    class Meta:
        queryset = PlayerSession.objects.all()
        resource_name = 'player-session'
        authorization = Authorization()
        filtering = {'name': ['icontains']}