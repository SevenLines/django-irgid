

def debug(context):
    from django.conf import settings
    return {
        'DEBUG': settings.DEBUG,
        'DONT_USE_METRICS': settings.DONT_USE_METRICS
    }


def custom_settings(context):
    from custom_settings.models import Setting
    settings = Setting.objects.filter(key__in=('headers_excursions', 'headers_travel'))

    out = {}

    for setting in settings:
        value = setting.get_value()
        items = value.split('/')
        while len(items) < 5:
            items.append('')

        out[setting.key] = {
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
