from __future__ import absolute_import

import os

from celery import Celery
import dotenv

dotenv.read_dotenv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tellylog.settings')

from django.conf import settings  # noqa

app = Celery('tellylog.celery')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
