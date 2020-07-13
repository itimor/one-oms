# -*- coding: utf-8 -*-
# author: itimor

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.utils import timezone
from celery_tasks import celeryconfig
from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
celery_app = Celery('celery_tasks', result_backend='django-db')
# celery_app = Celery('celery_tasks', backend='redis://127.0.0.1:6379', broker='redis://127.0.0.1:6379')
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')
# 从单独的配置模块中加载配置
celery_app.config_from_object(celeryconfig)
# 自动加载任务
celery_app.autodiscover_tasks([
    'celery_tasks',
])
celery_app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'

# 解决时区问题,定时任务启动就循环输出
celery_app.now = timezone.now
