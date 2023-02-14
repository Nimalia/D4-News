import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'when_creating_post': {
        'task': 'newsandart.tasks.send_message',
        'schedule': 30,
    },
}


# app.conf.beat_schedule = {
#     'weekly_subscribe': {
#         'task': 'newsandart.tasks.my_job',
#         'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
#     },
# }
app.conf.beat_schedule = {
    'weekly_subscribe': {
        'task': 'newsandart.tasks.my_job',
        'schedule': crontab(minute="*/1"),
    },
}