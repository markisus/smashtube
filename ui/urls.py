from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), 
    url(r'submit-youtube-link$', views.submit_youtube_link, name='submit-youtube-link'),
    url(r'submit-set-for-link/(\d+)$', views.submit_set_for_link, name='submit-set-for-link'),
    url(r'link-details/(\d+)$', views.link_details, name='link-details'),
    url(r'update$', views.update, name='update'), 
    url(r'populate$', views.populate, name='populate')
)