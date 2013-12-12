from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'), 
    url(r'update$', views.update, name='update'), 
)