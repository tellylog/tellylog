from __future__ import absolute_import
import logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('tmdbcall.log')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s -'
                              '%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
