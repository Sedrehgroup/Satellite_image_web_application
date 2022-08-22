from celery import Celery
from datetime import timedelta
import os
from celery.schedules import crontab
# import apis.tasks


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.autodiscover_tasks(['apis.tasks'])

celery_app.conf.broker_url = 'amqp://rabbitmq'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.CELERY_BEAT_SCHEDULER = 'django-celery-beat.schedulers.DatabaseScheduler'

# celery_app.conf.CELERY_BEAT_SCHEDULE = {
#     "delete_task": {
#         "task": "apis.tasks.delete_images",
#         "schedule": crontab(minute='*/1'),
#     },
# }