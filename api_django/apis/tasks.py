from celery import shared_task
import shutil
import os
from django.conf import settings
from celery.utils.log import get_task_logger
from geoserver import geoserver
import requests


logger = get_task_logger(__name__)


@shared_task(autoretry_for=(Exception,))
def delete_images():
    dir_path = os.path.join(settings.BASE_DIR , 'images')
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path,ignore_errors=True)
    geoserver.delete_workspace(settings.GEOSERVER.get('WORKSPACE'))
    logger.info('delete images ran!')