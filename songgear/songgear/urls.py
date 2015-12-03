from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.http import HttpResponseRedirect

from web import urls as web_urls
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/$', include(web_urls, namespace='web')),
    url(r'^/$', include('django.contrib.auth.urls')),
                       
)
