from django.conf import settings


def debug(context):
    return {
        'DEBUG': settings.DEBUG,
        'DONT_USE_METRICS': settings.DONT_USE_METRICS
    }
