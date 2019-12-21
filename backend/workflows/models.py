# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from systems.models import User


class Workflow(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name=u'名称')
    status = models.BooleanField(default=True)
    memo = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = '工作流'


class WorkflowStep(models.Model):
    workflow = models.ForeignKey(Workflow, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'工作流')
    name = models.CharField(max_length=32, unique=True, verbose_name=u'名称')
    action_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'执行者')
    sequence = models.SmallIntegerField(default=1, verbose_name=u'排序值')
    memo = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['sequence']
        verbose_name = '工作流步骤'
        verbose_name_plural = '工作流步骤'


status_type = (
    (1, '待提交'),
    (2, '审核中'),
    (3, '审核驳回'),
    (4, '执行中'),
    (5, '执行驳回'),
    (6, '执行完成'),
    (7, '完成关闭'),
    (8, '驳回关闭'),
    (9, '撤销关闭'),
)


class Ticket(models.Model):
    workflow = models.ForeignKey(Workflow, null=True, on_delete=models.SET_NULL, verbose_name=u'工作流')
    pid = models.IntegerField(unique=True, blank=True, verbose_name=u'工单号')
    name = models.CharField(max_length=32, unique=True, verbose_name=u'名称')
    content = models.TextField(blank=True, verbose_name=u'工单内容')
    status = models.CharField(max_length=1, choices=status_type, default=1, verbose_name=u'状态类型')
    create_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')
    step = models.SmallIntegerField(default=1, verbose_name=u'当前步骤')
    memo = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = '工单'
        verbose_name_plural = '工单'


class TicketReply(models.Model):
    ticket = models.ForeignKey(Ticket, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    content = models.TextField(blank=True, verbose_name=u'工单内容')
    create_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=u'创建者')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return '{}-->{}'.format(self.ticket, self.id)

    class Meta:
        verbose_name = '工单回复'
        verbose_name_plural = '工单回复'
