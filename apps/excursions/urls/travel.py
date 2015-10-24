from __future__ import absolute_import
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from excursions.views import ExcursionTravelIndexView, ExcursionTravelItemView

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',
    url(r'(?P<pk>(\d+))/$', ExcursionTravelItemView.as_view(), name='item'),
    url(r'$', ExcursionTravelIndexView.as_view(), name='index'),
)