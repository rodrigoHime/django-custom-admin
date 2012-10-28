from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="base.html")),	
	url(r'^grappelli/', include('grappelli.urls')),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    # url(r'^$', 'testGrappelli.views.home', name='home'),
)
