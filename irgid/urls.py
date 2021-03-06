# coding=utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

import custom_settings.urls
import excursions.urls.excursions
import excursions.urls.gallery
import excursions.urls.travel
import excursions.views.base
import sharedcontroll.urls
import django.contrib.auth.urls
import django.views.static
import django.contrib.staticfiles.urls
from excursions.models import Excursion, ExcursionCategory
from excursions.sitemaps import ExcursionsSitemap, ExcursionsCategorySitemap, \
    ExcursionsTravelSitemap, ExcursionsGallerySitemap, StaticViewSitemap, CalendarSitemap
from excursions.views import ExcursionCalendarView, ExcursionOffersList, SetLanguage
from irgid.views import TemplateViewEx, UploadFile

admin.autodiscover()


sitemaps = {
    'static': StaticViewSitemap(),
    'excursions': ExcursionsSitemap(),
    'excursions-travel': ExcursionsTravelSitemap(),
    'excursions-gallery': ExcursionsGallerySitemap(),
    'excursions-categories': ExcursionsCategorySitemap(),
    'calendar': CalendarSitemap(),
    # 'cmspages': CMSSitemap,
}

urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload-image/', UploadFile.as_view(), name='upload-image'),
    url(r'^excursions/', include(excursions.urls.excursions, namespace='excursions')),
    url(r'^gallery/', include(excursions.urls.gallery, namespace='gallery')),
    url(r'^travel/', include(excursions.urls.travel, namespace='travel')),
    url(r'^yandex-offers.xml$', ExcursionOffersList.as_view(), name='yandex-offers'),

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

    url(r'^calendar/$', ExcursionCalendarView.as_view(), name='calendar'),

    url(r'^faq/$', TemplateViewEx.as_view(
        template_name="faq.html", data={'title': u'FAQ'}
    ), name='faq'),


    url('^$', excursions.views.MainPageView.as_view(), name='index'),
    url('^', include(django.contrib.auth.urls)),
    # url(r'^', include('cms.urls')),
    prefix_default_language=False
)

urlpatterns += (
    url(r'set-language/(?P<lang>\w+)$', SetLanguage.as_view(), name='set_language'),
    url('i18n/', include('django.conf.urls.i18n', app_name="i18n", namespace="i18n")),
)


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', django.views.static.serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include(django.contrib.staticfiles.urls)),
    ]
