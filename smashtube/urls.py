from django.conf.urls import patterns, include, url
from django.conf import settings
from tastypie.api import Api
from smashconstants.api import GameTitleResource, CharacterResource, CharacterIconResource
from smashgames.api import TournamentResource
import ui.urls

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(GameTitleResource())
v1_api.register(CharacterResource())
v1_api.register(CharacterIconResource())
v1_api.register(TournamentResource())

urlpatterns = patterns('',
    # Examples:
    url(r'', include(ui.urls)),
    url(r'^api/', include(v1_api.urls)),
    # url(r'^$', 'smashtube.views.home', name='home'),
    # url(r'^smashtube/', include('smashtube.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)