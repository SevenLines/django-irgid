from django.core.cache import cache
from polymorphic.managers import PolymorphicManager


class CustomSettingsCacheManager(PolymorphicManager):
    def get_value(self, key):
        value = cache.get(key)
        if not value:
            value = self.get(key=key).get_value()
            cache.set(key, value)
        return value
