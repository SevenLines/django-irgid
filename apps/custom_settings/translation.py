from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register

from custom_settings.models import TextSetting


@register(TextSetting)
class TextSettingTranslationOptions(TranslationOptions):
    fields = ('value', )