# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from common.models import BaseModel


class CDN(BaseModel):
    name = models.CharField(max_length=112, unique=True, verbose_name='CDN厂商')
    code = models.CharField(max_length=112, unique=True, verbose_name='CDN英文')
    status = models.BooleanField(default=True, verbose_name=u'状态')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "CDN厂商"
        verbose_name_plural = verbose_name


class IPPool(BaseModel):
    cdn = models.ForeignKey(CDN, on_delete=models.CASCADE, verbose_name='CDN厂商')
    ip = models.CharField(max_length=255, unique=True, verbose_name='IP')

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['-create_time']
        verbose_name = "边缘节点IP"
        verbose_name_plural = verbose_name


class Project(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name='名称')
    code = models.CharField(max_length=112, unique=True, verbose_name='code')
    status = models.BooleanField(default=True, verbose_name=u'状态')
    keyword = models.CharField(max_length=255, verbose_name='关键字')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-create_time']
        verbose_name = "域名品牌"
        verbose_name_plural = verbose_name


domain_type = (
    ('web', 'pc端'),
    ('h5', '移动端'),
    ('appdown', 'app下载'),
    ('agent', '代理'),
)


class Domain(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='品牌')
    domain = models.CharField(max_length=255, verbose_name='域名')
    type = models.CharField(max_length=1, choices=domain_type, default='web', verbose_name=u'类型')

    def __str__(self):
        return self.domain

    class Meta:
        ordering = ['-create_time']
        verbose_name = "域名管理"
        verbose_name_plural = verbose_name

    # def save(self, *args, **kwargs):
    #     import re
    #     if not re.match(r'^(http|https)?://\w.+$', self.domain):
    #         self.domain = 'http://{}'.format(self.domain)
    #     super(Domain, self).save(*args, **kwargs)
