from __future__ import absolute_import, unicode_literals
import os
import sys
sys.path.append(os.path.relpath('apps'))

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from irgid.celery import app as celery_app

__all__ = ['celery_app']
