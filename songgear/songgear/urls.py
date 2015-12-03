from django.conf.urls import patterns, include, url
from django.contrib import admin

from web import urls as web_urls
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^web/', include(web_urls, namespace='web')),
    url(r'^web/', include('django.contrib.auth.urls')),
)
