from django.utils.translation import get_language


def debug(context):
    from django.conf import settings
    return {
        'DEBUG': settings.DEBUG,
        'DONT_USE_METRICS': settings.DONT_USE_METRICS,
    }


def custom_settings(context):
    from custom_settings.models import Setting
    settings = {
        'headers_excursions': Setting.objects.get_value('headers_excursions'),
        'headers_travel': Setting.objects.get_value('headers_travel'),
    }

    out = {}

    for key, value in settings.items():
        items = value.split('/')
        while len(items) < 5:
            items.append('')

        out[key] = {
            'people': items[0],
            'default_price': items[1],
            'price_line': {
                0: items[4],
                1: items[3],
                2: items[2],
            }
        }

    out['CUSTOMS'] = out
    return out

def language(context):
    lang = get_language()
    return {
        "LANGUAGE": lang
    }