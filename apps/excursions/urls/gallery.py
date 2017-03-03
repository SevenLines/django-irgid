from __future__ import absolute_import
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from excursions.views import ExcursionGalleryItemView, ExcursionGalleryIndexView

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',
    url(r'(?P<pk>(\d+))/(?P<title>(.*?)$)', ExcursionGalleryItemView.as_view(), name='item'),
    url(r'(?P<pk>(\d+))/$', ExcursionGalleryItemView.as_view(), name='item'),
    url(r'$', ExcursionGalleryIndexView.as_view(), name='index'),
)
