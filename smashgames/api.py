# myapp/api.py
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.validation import FormValidation
from tastypie import fields
from models import Tournament, Set, Match, VideoURL, Player, PlayerSession
from forms import TournamentForm
from smashconstants.api import GameTitleResource, CharacterResource

class TournamentResource(ModelResource):
    class Meta:
        queryset = Tournament.objects.all()
        resource_name = 'tournament'
        authorization = Authorization()
        validation = FormValidation(form_class=TournamentForm)
        filtering = {'name': ['icontains']}

class SetResource(ModelResource):
    tournament = fields.ForeignKey(TournamentResource, 'tournament', full=True, null=True)
    matches = fields.ToManyField('smashgames.api.MatchResource', 'matches', full=True)
    game_title = fields.ForeignKey(GameTitleResource, 'game_title', full=True)
    player_sessions = fields.ToManyField('smashgames.api.PlayerSessionResource', 'player_sessions', full=True)
    
    class Meta:
        queryset = Set.objects.all()
        resource_name = 'set'
        authorization = Authorization()
        filtering = {'description': ['icontains'],
                     'matches': ALL_WITH_RELATIONS}
        ordering = ['id']
                     
    def get_object_list(self, request):
        return super(SetResource, self).get_object_list(request).distinct()

class MatchResource(ModelResource):
    set = fields.ForeignKey(SetResource, 'set', related_name='matches')
    video_url = fields.ForeignKey(VideoURLResource, 'video_url', full=True)

    class Meta:
        queryset = Match.objects.all()
        resource_name = 'match'
        authorization = Authorization()
        filtering = {'name': ['icontains'],
                     'id': ALL,
                     'video_url': ALL_WITH_RELATIONS}

class PlayerResource(ModelResource):
    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'
        authorization = Authorization()
        filtering = {'name': ['icontains']}

class PlayerSessionResource(ModelResource):
    set = fields.ForeignKey(SetResource, 'set')
    player = fields.ForeignKey(PlayerResource, 'player', full=True)
    character = fields.ForeignKey(CharacterResource, 'character', full=True)
    class Meta:
        queryset = PlayerSession.objects.all()
        resource_name = 'player-session'
        authorization = Authorization()
        filtering = {'match': ALL_WITH_RELATIONS}