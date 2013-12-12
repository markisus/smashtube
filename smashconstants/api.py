# myapp/api.py
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from models import *

class GameTitleResource(ModelResource):
    class Meta:
        queryset = GameTitle.objects.all()
        resource_name = 'gametitle'

class CharacterResource(ModelResource):
    class Meta:
        queryset = Character.objects.all()
        resource_name = 'character'

class CharacterIconResource(ModelResource):
    class Meta:
        queryset = CharacterIcon.objects.all()
        resource_name = 'charactericon'