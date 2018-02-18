from django.core.cache import cache
from django.utils.translation import get_language
from polymorphic.managers import PolymorphicManager


class CustomSettingsCacheManager(PolymorphicManager):
    def get_value(self, key):
        lang = get_language()
        key_lang = "{}_{}".format(key, lang)
        value = cache.get(key_lang)
        if not value:
            value = self.get(key=key).get_value()
            cache.set(key_lang, value)
        return value

