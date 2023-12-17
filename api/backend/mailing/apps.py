from django.apps import AppConfig
from backend.celery import *
from celery.schedules import crontab


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        app.conf.beat_schedule = {
            'every': {
                'task': "mailing.tasks.check_mailings",
                'schedule': crontab(),
            },
        }
