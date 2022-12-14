from celery import Celery
from celery.schedules import crontab

import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sagivor.settings')

app = Celery('sagivor')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'update-create-every-10-minutes': {  # создание таска, который будет проверять доступность формы
        'task': 'bot.tasks.form_check',
        'schedule': 600,
    }
}
app.conf.timezone = 'Asia/Bishkek'
