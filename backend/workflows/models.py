# -*- coding: utf-8 -*-
# author: itimor

from django.db import models


class Workflow(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=u'角色')
    status = models.BooleanField(default=True)
    memo = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = '工作流'
