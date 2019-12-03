# -*- coding: utf-8 -*-
# author: timor

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


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


class User(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True, db_index=True)
    realname = models.CharField(max_length=32, blank=True, verbose_name=u'真实名字')
    avator = models.CharField(max_length=255, default='http://m.imeitou.com/uploads/allimg/2017110610/b3c433vwhsk.jpg')
    roles = models.ManyToManyField('Role', blank=True, verbose_name=u'角色')
    create_date = models.DateField(auto_now_add=True, verbose_name=u'创建时间')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'  # 必须有一个唯一标识--USERNAME_FIELD

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'

    objects = UserManager()  # 创建用户


class Role(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, default='1', verbose_name=u'父级角色')
    name = models.CharField(max_length=32, unique=True, verbose_name=u'角色')
    sequence = models.SmallIntegerField(default=0, verbose_name=u'排序值')
    menus = models.ManyToManyField('Menu', blank=True, verbose_name=u'菜单')
    desc = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色'


menu_type = (
    ('1', '模块'),
    ('2', '菜单'),
    ('3', '操作'),
)

menu_status = (
    ('1', '启用'),
    ('2', '禁用'),
)

operate_type = (
    ('none', '无'),
    ('add', '增'),
    ('del', '删'),
    ('update', '改'),
    ('view', '查'),
)


class Menu(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, default='1', verbose_name=u'父级菜单')
    name = models.CharField(max_length=32, verbose_name=u'菜单名称')
    code = models.CharField(max_length=32, verbose_name=u'菜单代码')
    curl = models.CharField(max_length=101, verbose_name=u'菜单URL')
    icon = models.CharField(max_length=32, verbose_name=u'菜单图标')
    hidden = models.BooleanField(default=False, verbose_name=u'菜单是否隐藏')
    affix = models.BooleanField(default=True, verbose_name=u'是否显示tags-view')
    sequence = models.SmallIntegerField(default=0, verbose_name=u'排序值')
    type = models.CharField(max_length=1, choices=menu_type, default='2', verbose_name=u'菜单类型')
    status = models.CharField(max_length=1, choices=menu_status, default='1', verbose_name=u'菜单状态')
    operate = models.CharField(max_length=1, choices=operate_type, default='none', verbose_name=u'操作类型')
    desc = models.TextField(blank=True, verbose_name=u'备注')

    def __str__(self):
        return "{parent}{name}".format(name=self.name, parent="%s-->" % self.parent.name if self.parent else '')

    class Meta:
        verbose_name = u'角色'
        verbose_name_plural = u'角色'
