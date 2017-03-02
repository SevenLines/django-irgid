from __future__ import absolute_import

import os

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irgid.settings')


if settings.TESTING:
    task_always_eager = True
    task_eager_propagates = True
else:
    broker_url = 'amqp://guest:guest@localhost:5672//'


timezone = settings.TIME_ZONE

try:
    from .celery_config_local import *
except:
    pass
