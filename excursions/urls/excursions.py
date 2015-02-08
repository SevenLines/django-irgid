from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',

    url(r'excursion/(\d+)/remove/$', 'excursion_remove'),
    url(r'excursion/(\d+)/$', 'excursion'),
    url(r'excursion/gallery/(\d+)/$', 'excursion_gallery_item'),
    url(r'excursion/gallery$', 'excursion_gallery_index'),
    url(r'excursion/save/$', 'excursion_save'),
    url(r'excursion/ajax/save$', 'ajax.excursion_save'),
    url(r'excursion/image/add', 'ajax.excursion_image_add'),
    url(r'excursion/image/(\d+)/remove$', 'ajax.excursion_image_remove'),

    url(r'category/(\d+)/remove/$', 'category_remove'),
    url(r'category/(\d+)/$', 'category'),
    url(r'category/ajax/save/$', 'ajax.category_save'),
    url(r'category/save/$', 'category_save'),
    url(r'category/ajax/set-order/$', 'ajax.set_categories_order'),
    url(r'category/ajax/set-image/$', 'ajax.set_category_image'),
    url(r'category/ajax/remove-image/$', 'ajax.remove_category_image'),
    url(r'category/ajax/remove/$', 'ajax.category_remove'),
    url(r'category/ajax/toggle/$', 'ajax.toggle_category'),


    url(r'$', 'index'),
)
