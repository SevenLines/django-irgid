from cms.sitemaps.cms_sitemap import CMSSitemap
from django.conf.urls import include, patterns, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap

import custom_settings.urls
from excursions.models import Excursion, ExcursionCategory
import excursions.urls.excursions
import excursions.urls.gallery
import sharedcontroll.urls
import textpage.urls

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
    'cmspages': CMSSitemap,
}


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^excursions-app/', include(excursions.urls.excursions)),
    url(r'^gallery-app/', include(excursions.urls.gallery)),
    url(r'^settings/', include(custom_settings.urls)),
    url(r'^textpages-app/', include(textpage.urls)),
    url(r'^sharedcontroll-app/', include(sharedcontroll.urls)),
    url(r'login/', "app.views.login_user"),
    url(r'logout/', "django.contrib.auth.views.logout"),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^', include('cms.urls')),
)



if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns
