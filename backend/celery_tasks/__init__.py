# 如果有用到celery,开启下面注释
from celery_tasks.celery import celery_app
__all__ = ['celery_app']