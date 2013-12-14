from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), 
    url(r'submit-youtube-link$', views.submit_youtube_link, name='submit-youtube-link'),
    url(r'submit-set-for-link/(\d+)$', views.submit_set_for_link, name='submit-set-for-link'),
    url(r'submit-player-for-match$', views.submit_player_for_match, name='submit-player-for-match'),
    url(r'delete-player-session$', views.delete_player_session, name='delete-player-session'),
    url(r'edit-match$', views.edit_match, name='edit-match'),
    url(r'delete-match$', views.delete_match, name='delete-match'),
    url(r'copy-match$', views.copy_match, name='copy-match'),
    url(r'delete-set$', views.delete_set, name='delete-set'),
    url(r'delete-link$', views.delete_link, name='delete-link'),
    url(r'link-details/(\d+)$', views.link_details, name='link-details'),
    url(r'update$', views.update, name='update'), 
    url(r'populate$', views.populate, name='populate')
)