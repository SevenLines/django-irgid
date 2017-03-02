# coding=utf-8
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

import custom_settings.urls
import excursions.urls.excursions
import excursions.urls.gallery
import excursions.urls.travel
import excursions.views.base
import sharedcontroll.urls
from excursions.models import Excursion, ExcursionCategory
from excursions.views import ExcursionCalendarView
from irgid.views import TemplateViewEx, UploadFile

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
    url(r'^upload-image/', UploadFile.as_view(), name='upload-image'),
    url(r'^excursions/', include(excursions.urls.excursions, namespace='excursions', app_name='excursions')),
    url(r'^gallery/', include(excursions.urls.gallery, namespace='gallery', app_name='excursions')),
    url(r'^travel/', include(excursions.urls.travel, namespace='travel', app_name='excursions')),

    # for old urls comaptability
    url(r'^excursions-app/', include(excursions.urls.excursions)),
    url(r'^gallery-app/', include(excursions.urls.gallery)),

    url(r'^settings/', include(custom_settings.urls)),
    url(r'^sharedcontroll-app/', include(sharedcontroll.urls)),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    url(r'^about/$', TemplateViewEx.as_view(
        template_name="about.html", data={'title': u'О нас'}
    ), name='about'),

    url(r'^confedential/$', TemplateViewEx.as_view(
        template_name="confedential.html", data={'title': u'Политика конфиденциальности'}
    ), name='confedential'),

    # url(r'^calendar/$', TemplateViewEx.as_view(
    #     template_name="calendar.html", data={'title': u'Расписание экскурсий'}
    # ), name='calendar'),
    url(r'^calendar/$', ExcursionCalendarView.as_view(), name='calendar'),

    url(r'^faq/$', TemplateViewEx.as_view(
        template_name="faq.html", data={'title': u'FAQ'}
    ), name='faq'),

    url('^$', excursions.views.MainPageView.as_view(), name='index'),
    url('^', include('django.contrib.auth.urls')),
    # url(r'^', include('cms.urls')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
