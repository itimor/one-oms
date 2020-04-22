# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '初始化 菜单 角色 用户'

    def handle(self, *args, **options):
        users = User.objects.all()
        if len(users) == 0:
            self.stdout.write(self.style.SUCCESS('############初始化用户和角色###########'))
            try:
                user = User.objects.create(username='admin', password=make_password("qwert@12345"), is_admin=True)
                user.roles.create(name='top', code='top', sequence=0, parent_id=None)
            except:
                raise CommandError('初始化用户和角色失败')
        menus = Menu.objects.all()
        if len(menus) == 0:
            self.stdout.write(self.style.SUCCESS('############初始化菜单###########'))
            topmenu = Menu.objects.create(name='top', code='top', curl='/top', icon='top', sequence=0, type=1,
                                          parent_id=None)
            sysmenu = Menu.objects.create(name='系统管理', code='sys', curl='/sys', icon='sys', sequence=1, type=1,
                                          parent_id=topmenu.id)
            menumodel = Menu.objects.create(name='用户管理', code='user', curl='/user', icon='user', sequence=10, type=2,
                                            parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='角色管理', code='role', curl='/role', icon='role', sequence=20, type=2,
                                            parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='菜单管理', code='menu', curl='/menu', icon='menu', sequence=30, type=2,
                                            parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='图标管理', code='icon', curl='/icon', icon='icon', sequence=40, type=2,
                                            parent_id=sysmenu.id)
            init_menu(menumodel)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
