from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^songs/$', views.songs, name='songs'),
    url(r'^artists/$', views.artists, name='artists'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^(?P<pk>[0-9]+)/copy/$', views.copy, name='copy'),
    url(r'^new/$', views.new, name='new'),
    url(r'^new_artist/$', views.new_artist, name='new_artist'),
    url(r'^new_artist_ajax/$', views.new_artist_ajax, name='new_artist_ajax'),
    url(r'^new_genre_ajax/$', views.new_genre_ajax, name='new_genre_ajax'),
    url(r'^(?P<pk>[0-9]+)/edit_artist/$', views.edit_artist, name='edit_artist'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.delete, name='delete'),
    url(r'^(?P<pk>[0-9]+)/delete_comment/(?P<comment>[0-9]+)', views.delete_comment, name='delete_comment'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.register_confirm, name='confirm'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', views.reset_confirm, name='reset_confirm'),
    url(r'^reset/$', views.reset, name='reset'),
    url(r'^reset_sent/$', views.reset_sent, name='reset_sent')
]