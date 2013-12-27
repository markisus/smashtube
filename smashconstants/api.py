# myapp/api.py
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields
from models import *

class GameTitleResource(ModelResource):
    class Meta:
        queryset = GameTitle.objects.all()
        resource_name = 'game-title'
        filtering = {'id': ALL,
                    'name': ALL}

class CharacterResource(ModelResource):
    games = fields.ToManyField(GameTitleResource, 'games')
    
    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'
        filtering = {'games': ALL_WITH_RELATIONS}

class CharacterIconResource(ModelResource):
    class Meta:
        queryset = CharacterIcon.objects.all()
        resource_name = 'character-icon'