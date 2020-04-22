# -*- coding: utf-8 -*-
# author: itimor

from django.db import models


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    memo = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        ordering = ('-create_time',)
        abstract = True

