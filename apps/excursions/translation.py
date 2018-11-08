from modeltranslation.decorators import register
from modeltranslation.translator import TranslationOptions

from excursions.models import Excursion, ExcursionCategory


@register(Excursion)
class ExcursionTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
        'short_description',
        'published',
    )
    fallback_undefined = {'published': None}


@register(ExcursionCategory)
class ExcursionCategoryTranslationOptions(TranslationOptions):
    fields = (
        'title',
        'description',
        'visible',
    )
