from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',

    url(r'excursion/(\d+)/remove/$', 'excursion_remove'),
    url(r'excursion/(\d+)/$', 'excursion'),
    url(r'excursion/save/$', 'excursion_save'),
    url(r'excursion/ajax/save$', 'ajax.excursion_save'),
    url(r'excursion/image/add', 'ajax.excursion_image_add'),
    url(r'excursion/image/remove', 'ajax.excursion_image_remove'),

    url(r'category/(\d+)/remove/$', 'category_remove'),
    url(r'category/(\d+)/$', 'category'),
    url(r'category/save/$', 'category_save'),


    url(r'$', 'index'),
)