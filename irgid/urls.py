# coding=utf-8
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

import custom_settings.urls
import excursions.urls.excursions
import excursions.urls.gallery
import excursions.views.base
import sharedcontroll.urls
from excursions.models import Excursion, ExcursionCategory
from irgid.views import TemplateViewEx

admin.autodiscover()


sitemaps = {
    'excursions': GenericSitemap({
        'queryset': Excursion.objects.all(),
        'data_field': 'update_date',
        'changefreq': 'weekly',
    }),
    'excursions-categories': GenericSitemap({
        'queryset': ExcursionCategory.objects.all(),
        'data_field': 'update_date',
        'changefreq': 'weekly',
    }),
    # 'cmspages': CMSSitemap,
}


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^excursions/', include(excursions.urls.excursions, namespace='excursions', app_name='excursions')),
    url(r'^gallery/', include(excursions.urls.gallery, namespace='gallery', app_name='excursions')),

    # for old urls comaptability
    url(r'^excursions-app/', include(excursions.urls.excursions)),
    url(r'^gallery-app/', include(excursions.urls.gallery)),

    url(r'^settings/', include(custom_settings.urls)),
    url(r'^sharedcontroll-app/', include(sharedcontroll.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^about/$', TemplateViewEx.as_view(template_name="about.html", data={'title': u'О нас'}), name='about'),
    url(r'^faq/$', TemplateViewEx.as_view(template_name="faq.html", data={'title': u'FAQ'}), name='faq'),
    url('^$', excursions.views.index, name='index'),
    url('^', include('django.contrib.auth.urls')),
    # url(r'^', include('cms.urls')),
)



if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
