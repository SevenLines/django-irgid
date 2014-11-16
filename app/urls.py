from django.conf.urls.defaults import *
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = i18n_patterns('',
                            (r'^robots\.txt$', TemplateView.as_view(
                                template_name='robots.txt', content_type='text/plain')),
                            (r'^sitemap\.xml$', TemplateView.as_view(
                                template_name='sitemap.xml', content_type='text/plain')),
                            url(r'^gallery/', include('image_gallery.urls')),
                            url(r'^admin/', include(admin.site.urls)),
                            url(r'^', include('cms.urls')),
                            )

if settings.DEBUG:
    urlpatterns = patterns('',
                           url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                               {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                           url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
