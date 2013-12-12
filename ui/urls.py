from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), 
    url(r'submit-youtube-link$', views.submit_youtube_link, name='submit-youtube-link'),
    url(r'update$', views.update, name='update'), 

)