from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',
    url(r'(\d+)/$', 'excursion_gallery_item', name='item'),
    url(r'$', 'excursion_gallery_index', name='index'),
)
