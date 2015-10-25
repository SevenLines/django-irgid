# coding=utf-8
from __future__ import absolute_import
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from excursions.views import MainPageView, CategoryView, ExcursionItemView, ExcursionGalleryItemView, \
    ExcursionGalleryIndexView

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',
    url(r'c/(?P<pk>(\d+))/remove/$', 'category_remove', name='category_remove'),
    url(r'c/(?P<pk>(\d+))/$', CategoryView.as_view(), name='category'),
    url(r'c/ajax/save/$', 'ajax.category_save', name='ajax_category_save'),
    url(r'c/ajax/set-order/$', 'ajax.set_categories_order', name='ajax_set_categories_order'),
    url(r'c/ajax/set-image/$', 'ajax.set_category_image', name='ajax_set_category_image'),
    url(r'c/ajax/remove-image/$', 'ajax.remove_category_image', name='ajax_remove_category_image'),
    url(r'c/ajax/remove/$', 'ajax.category_remove', name='ajax_category_remove'),
    url(r'c/ajax/toggle/$', 'ajax.toggle_category', name='ajax_toggle_category'),
    url(r'c/save/$', 'category_save', name='category_save'),

    url(r'save/$', 'excursion_save', name='save'),
    url(r'ajax/save$', 'ajax.excursion_save', name='ajax_save'),
    url(r'image/add', 'ajax.excursion_image_add', name='image_add'),
    url(r'image/(\d+)/remove$', 'ajax.excursion_image_remove', name='ajax_image_remove'),
    url(r'(?P<pk>(\d+))/remove/$', 'excursion_remove', name='remove'),
    url(r'(?P<pk>(\d+))/$', ExcursionItemView.as_view(), name='item'),

    url(r'$', MainPageView.as_view(), name='index'),

    # для совместимости со старой версией ссылок
    url(r'excursion/(?P<pk>(\d+))/remove/$', 'excursion_remove'),
    url(r'excursion/(?P<pk>(\d+))/$', ExcursionItemView.as_view()),
    url(r'excursion/gallery/(?P<pk>(\d+))/$', ExcursionGalleryItemView.as_view()),
    url(r'excursion/gallery$', ExcursionGalleryIndexView.as_view()),
    url(r'excursion/save/$', 'excursion_save'),
    url(r'excursion/ajax/save$', 'ajax.excursion_save'),
    url(r'excursion/image/add', 'ajax.excursion_image_add'),
    url(r'excursion/image/(?P<pk>(\d+))/remove$', 'ajax.excursion_image_remove'),

    url(r'category/(?P<pk>(\d+))/remove/$', 'category_remove'),
    url(r'category/(?P<pk>(\d+))/$', CategoryView.as_view()),
    url(r'category/ajax/save/$', 'ajax.category_save'),
    url(r'category/save/$', 'category_save'),
    url(r'category/ajax/set-order/$', 'ajax.set_categories_order'),
    url(r'category/ajax/set-image/$', 'ajax.set_category_image'),
    url(r'category/ajax/remove-image/$', 'ajax.remove_category_image'),
    url(r'category/ajax/remove/$', 'ajax.category_remove'),
    url(r'category/ajax/toggle/$', 'ajax.toggle_category'),

)
