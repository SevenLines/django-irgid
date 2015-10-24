from django.db import models

from custom_settings.models import Setting


class ExcursionsCategoryManager(models.Manager):
    def _data(self, excluded, user):
        excluded_pk = [item.value for item in excluded]
        result = self.get_queryset().exclude(pk__in=excluded_pk).order_by('order', 'title')
        if not user or not user.is_authenticated():
            result = result.filter(visible=True)
        return result

    def common(self, user=None):
        excluded = Setting.objects.filter(key__in=('gallery_id', 'travel_id'))
        return self._data(excluded, user)

    def common_with_gallery(self, user=None):
        excluded = Setting.objects.filter(key__in=('travel_id'))
        return self._data(excluded, user)

    def gallery(self):
        return self.get_queryset().filter(pk=Setting.objects.get(key='gallery_id').get_value()).last()

    def travel(self):
        return self.get_queryset().filter(pk=Setting.objects.get(key='travel_id').get_value()).last()