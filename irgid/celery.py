from __future__ import absolute_import
from celery import Celery

app = Celery('irgid')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('irgid.celery_config')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
