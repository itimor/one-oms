# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from common.models import BaseModel


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        username 是唯一标识，没有会报错
        """

        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
        )
        user.set_password(password)  # 检测密码合理性
        user.save(using=self._db)  # 保存密码
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username,
                                password=password,
                                )
        user.is_admin = True  # 比创建用户多的一个字段
        user.save(using=self._db)
        return user


class User(BaseModel, AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, db_index=True)
    realname = models.CharField(max_length=32, blank=True, verbose_name=u'真实名字')
    avatar = models.CharField(max_length=255, default='http://m.imeitou.com/uploads/allimg/2017110610/b3c433vwhsk.jpg')
    roles = models.ManyToManyField('Role', blank=True, verbose_name=u'角色')
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        ordering = ['-create_time']
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    objects = UserManager()  # 创建用户


class Role(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, default='0', verbose_name=u'父级角色')
    name = models.CharField(max_length=32, unique=True, verbose_name=u'名称')
    code = models.CharField(max_length=32, unique=True, verbose_name=u'代码')
    sequence = models.SmallIntegerField(default=0, verbose_name=u'排序值')
    menus = models.ManyToManyField('Menu', blank=True, verbose_name=u'菜单')
    apiperms = models.ManyToManyField('ApiPerm', blank=True, verbose_name=u'api权限')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        ordering = ['-create_time']
        verbose_name = '角色'
        verbose_name_plural = verbose_name


menu_type = (
    (1, '模块'),
    (2, '菜单'),
    (3, '操作'),
)

operate_type = (
    ('none', '无'),
    ('add', '新增'),
    ('del', '删除'),
    ('update', '编辑'),
    ('view', '查看'),
)


class Menu(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, default='0', verbose_name=u'父级菜单')
    name = models.CharField(max_length=32, verbose_name=u'菜单名称')
    code = models.CharField(max_length=32, verbose_name=u'菜单代码')
    curl = models.CharField(max_length=101, verbose_name=u'菜单URL')
    icon = models.CharField(max_length=32, blank=True, verbose_name=u'菜单图标')
    hidden = models.BooleanField(default=False, verbose_name=u'菜单是否隐藏')
    sequence = models.SmallIntegerField(default=0, verbose_name=u'排序值')
    type = models.CharField(max_length=1, choices=menu_type, default=2, verbose_name=u'菜单类型')
    status = models.BooleanField(default=True, verbose_name=u'状态')
    operate = models.CharField(max_length=5, choices=operate_type, default='none', verbose_name=u'操作类型')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        ordering = ['id', ]
        verbose_name = '角色'
        verbose_name_plural = verbose_name


class ApiPerm(BaseModel):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, default='0', verbose_name=u'父级角色')
    name = models.CharField(max_length=32, unique=True, verbose_name=u'名称')
    method = models.CharField(max_length=32, verbose_name=u'请求方法')
    curl = models.CharField(max_length=101, verbose_name=u'请求路径')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        ordering = ['-create_time']
        verbose_name = u'api权限'
        verbose_name_plural = verbose_name
