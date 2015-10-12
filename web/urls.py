from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^new/$', views.new, name='new'),
    url(r'^new_artist/$', views.new_artist, name='new_artist'),
    url(r'^(?P<pk>[0-9]+)/edit_artist/$', views.edit_artist, name='edit_artist'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/web/'}, name='logout'),
]