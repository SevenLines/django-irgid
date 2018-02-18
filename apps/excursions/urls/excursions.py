# coding=utf-8
from __future__ import absolute_import
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

from excursions.views import MainPageView, CategoryView, ExcursionItemView, ExcursionGalleryItemView, \
    ExcursionGalleryIndexView, ExcursionRemoveView, ExcursionCategoryRemoveView, ExcursionPreviewItemView, \
    ExcursionCalendarView, ExcursionCalendarUpdateView, ExcursionAppointmentCreateView
from excursions.views.ajax import ExcursionMainImageRemove

__author__ = 'm'
import excursions.views as v

urlpatterns = [
    url(r'c/ajax/save/$', v.ajax.category_save, name='ajax_category_save'),
    url(r'c/ajax/set-order/$', v.ajax.set_categories_order, name='ajax_set_categories_order'),
    url(r'c/ajax/set-image/$', v.ajax.set_category_image, name='ajax_set_category_image'),
    url(r'c/ajax/remove-image/$', v.ajax.remove_category_image, name='ajax_remove_category_image'),
    # url(r'c/ajax/remove/$', excursions.views.ajax.category_remove', name='ajax_category_remove'),
    url(r'c/ajax/toggle/$', v.ajax.toggle_category, name='ajax_toggle_category'),
    url(r'c/save/$', v.category_save, name='category_save'),
    url(r'c/(?P<pk>(\d+))/remove/$', ExcursionCategoryRemoveView.as_view(), name='category_remove'),
    url(r'c/(?P<pk>(\d+))/(?P<title>.*?)$', CategoryView.as_view(), name='category'),
    url(r'c/(?P<pk>(\d+))/$', CategoryView.as_view(), name='category'),

    url(r'save/$', v.excursion_save, name='save'),
    url(r'ajax/save$', v.ajax.excursion_save, name='ajax_save'),
    url(r'image/add$', v.ajax.excursion_image_add, name='image_add'),
    url(r'image/(?P<pk>(\d+))/remove$', v.ajax.excursion_image_remove, name='ajax_image_remove'),
    url(r'image/(?P<pk>(\d+))/toggle$', v.ajax.excursion_image_toggle, name='ajax_image_toggle'),
    url(r'(?P<pk>(\d+))/main-image-remove/$', ExcursionMainImageRemove.as_view(), name='ajax_main_image_remove'),
    url(r'(?P<pk>(\d+))/remove/$', ExcursionRemoveView.as_view(), name='remove'),
    url(r'(?P<pk>(\d+))/preview/$', ExcursionPreviewItemView.as_view(), name='item_preview'),
    url(r'(?P<pk>(\d+))/(?P<title>.*?)$', ExcursionItemView.as_view(), name='item'),
    url(r'(?P<pk>(\d+))/$', ExcursionItemView.as_view(), name='item'),

    url(r'calendar/update$', ExcursionCalendarUpdateView.as_view(), name='calendar_update'),
    url(r'calendar/$', ExcursionCalendarView.as_view(), name='calendar'),

    url(r'appointment/$', ExcursionAppointmentCreateView.as_view(), name='appointment_create'),
    url(r'set-language/(?P<lang>\w+)$', v.SetLanguage.as_view(), name='set_language'),

    url(r'$', MainPageView.as_view(), name='index'),

    # для совместимости со старой версией ссылок
    url(r'excursion/(?P<pk>(\d+))/remove/$', ExcursionRemoveView.as_view()),
    url(r'excursion/(?P<pk>(\d+))/$', ExcursionItemView.as_view()),
    url(r'excursion/gallery/(?P<pk>(\d+))/$', ExcursionGalleryItemView.as_view()),
    url(r'excursion/gallery$', ExcursionGalleryIndexView.as_view()),
    url(r'excursion/save/$', v.excursion_save),
    url(r'excursion/ajax/save$', v.ajax.excursion_save),
    url(r'excursion/image/add$', v.ajax.excursion_image_add),
    url(r'excursion/image/(?P<pk>(\d+))/remove$', v.ajax.excursion_image_remove),

    url(r'category/(?P<pk>(\d+))/remove/$', ExcursionCategoryRemoveView.as_view()),
    url(r'category/(?P<pk>(\d+))/$', CategoryView.as_view()),
    url(r'category/ajax/save/$', v.ajax.category_save),
    url(r'category/save/$', v.category_save),
    url(r'category/ajax/set-order/$', v.ajax.set_categories_order),
    url(r'category/ajax/set-image/$', v.ajax.set_category_image),
    url(r'category/ajax/remove-image/$', v.ajax.remove_category_image),
    url(r'category/ajax/toggle/$', v.ajax.toggle_category),
]
