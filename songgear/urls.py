from django.conf.urls import patterns, include, url
from django.contrib import admin
from web import urls as web_urls
from web.viewsets import UserViewSet, SongViewSet, ArtistViewSet, GenreViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'songs', SongViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'genres', GenreViewSet)

urlpatterns = patterns('',
    url(r'', include(web_urls, namespace='web')),
    url(r'', include('django.contrib.auth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))


)
