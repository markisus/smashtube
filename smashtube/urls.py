from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from smashconstants.api import GameTitleResource, CharacterResource, CharacterIconResource
from smashgames.api import TournamentResource, SetResource, MatchResource, \
    PlayerResource, PlayerSessionResource, VideoURLResource
import ui.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(GameTitleResource())
v1_api.register(CharacterResource())
v1_api.register(CharacterIconResource())
v1_api.register(TournamentResource())
v1_api.register(SetResource())
v1_api.register(PlayerResource())
v1_api.register(PlayerSessionResource())
v1_api.register(VideoURLResource())
v1_api.register(MatchResource())

urlpatterns = patterns('',
    # Examples:
    url(r'', include(ui.urls)),
    url(r'^api/', include(v1_api.urls)),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)