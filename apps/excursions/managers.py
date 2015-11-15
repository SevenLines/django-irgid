from django.db import models

from custom_settings.models import Setting, IntegerSetting
from django.core.cache import cache


class ExcursionsCategoryManager(models.Manager):
    def get_gallery_id(self):
        gallery_id = cache.get('gallery_id')
        if not gallery_id:
            gallery_id = Setting.objects.get(key='gallery_id').get_value()
            cache.set('gallery_id', gallery_id)
        return gallery_id

    def get_travel_id(self):
        travel_id = cache.get('travel_id')
        if not travel_id:
            travel_id = Setting.objects.get(key='travel_id').get_value()
            cache.set('travel_id', travel_id)
        return travel_id

    def _data(self, excluded_pk, user):
        result = self.get_queryset().exclude(pk__in=filter(None, excluded_pk)).order_by('order', 'title')
        if not user or not user.is_authenticated():
            result = result.filter(visible=True)
        return result

    def common(self, user=None):
        excluded = [self.get_gallery_id(), self.get_travel_id()]
        return self._data(excluded, user)

    def common_with_gallery(self, user=None):
        excluded = [self.get_travel_id()]
        return self._data(excluded, user)

    def common_with_all(self, user=None):
        return self._data([], user)

    def gallery(self):
        gallery_id = self.get_gallery_id()
        return self.get_queryset().filter(pk=gallery_id).last()

    def travel(self):
        travel_id = self.get_travel_id()
        return self.get_queryset().filter(pk=travel_id).last()

    def get_special_categories_info(self):
        result = {
            'gallery_id': self.get_gallery_id(),
            'travel_id': self.get_travel_id(),
        }

        for key, value in result.items():
            if not value:
                del result[key]

        return result
