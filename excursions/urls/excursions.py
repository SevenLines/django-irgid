from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

__author__ = 'm'

urlpatterns = i18n_patterns('excursions.views',
    url(r'excursion/(\d+)/remove/$', 'excursion_remove', name='remove'),
    url(r'excursion/(\d+)/$', 'excursion', name='item'),
    url(r'excursion/gallery/(\d+)/$', 'excursion_gallery_item', name='gallery_item'),
    url(r'excursion/gallery$', 'excursion_gallery_index', name='gallery'),
    url(r'excursion/save/$', 'excursion_save', name='save'),
    url(r'excursion/ajax/save$', 'ajax.excursion_save', name='ajax_save'),
    url(r'excursion/image/add', 'ajax.excursion_image_add', name='image_add'),
    url(r'excursion/image/(\d+)/remove$', 'ajax.excursion_image_remove', name='ajax_image_remove'),

    url(r'category/(\d+)/remove/$', 'category_remove', name='category_remove'),
    url(r'category/(\d+)/$', 'category', name='category'),
    url(r'category/ajax/save/$', 'ajax.category_save', name='ajax_category_save'),
    url(r'category/save/$', 'category_save', name='category_save'),
    url(r'category/ajax/set-order/$', 'ajax.set_categories_order', name='ajax_set_categories_order'),
    url(r'category/ajax/set-image/$', 'ajax.set_category_image', name='ajax_set_category_image'),
    url(r'category/ajax/remove-image/$', 'ajax.remove_category_image', name='ajax_remove_category_image'),
    url(r'category/ajax/remove/$', 'ajax.category_remove', name='ajax_category_remove'),
    url(r'category/ajax/toggle/$', 'ajax.toggle_category', name='ajax_toggle_category'),

    url(r'$', 'index', name='index'),
)
