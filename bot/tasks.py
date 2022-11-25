import requests

from celery.utils.log import get_task_logger
from celery import shared_task

from sagivor.celery import app
from utils.class_redis import r
from con_file import URL

logger = get_task_logger(__name__)


@app.task
def form_check():
    logger.info("form checking")
    response = requests.get(URL)
    if response.status_code == 200:
        r.change_status_code_true()
        logger.info('status code is true')
    else:
        r.change_status_code_false()
        logger.error("STATUS CODE IS FALSE")
