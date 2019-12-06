# -*- coding: utf-8 -*-
# author: itimor

from systems.models import *


# 获取管理员权限下所有菜单
def get_menus_by_user(user):
    user_obj = User.objects.filter(username=user)

    if user_obj.first().is_admin:
        menus = Menu.objects.all()
        if len(menus) == 0:
            print("############初始化菜单###########")
            topmenu = Menu.objects.create(name='top', code='top', curl='/top', icon='top', sequence=0, type=1, parent_id=None)
            sysmenu = Menu.objects.create(name='系统管理', code='sys', curl='/sys', icon='sys', sequence=1, type=1, parent_id=topmenu.id)
            menumodel = Menu.objects.create(name='用户管理', code='user', curl='/user', icon='user', sequence=10, type=2, parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='角色管理', code='role', curl='/role', icon='role', sequence=20, type=2, parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='菜单管理', code='menu', curl='/menu', icon='menu', sequence=30, type=2, parent_id=sysmenu.id)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='图标管理', code='icon', curl='/icon', icon='icon', sequence=40, type=2, parent_id=sysmenu.id)
            init_menu(menumodel)
            menus = Menu.objects.all()
    else:
        user_role_list = user_obj.values('roles')
        user_menu_list = Role.objects.filter(id__in=user_role_list).values('menus')

        menuMap = dict()
        for item in user_menu_list:
            menu_info = Menu.objects.get(id=item['menus'])
            menuMap[menu_info.id] = menu_info

        for item in user_menu_list:
            menu_info = Menu.objects.get(id=item['menus'])
            if menu_info.parent_id in menuMap:
                continue
            user_menus = find_menu_daddy(menu_info.parent_id, menuMap)
        menus = [user_menus[i] for i in sorted(user_menus.keys())]
    return menus


def find_menu_daddy(menuid, menuMap):
    obj = Menu.objects.filter(id=menuid).first()
    if obj:
        mid = obj.id
        if mid not in menuMap:
            menuMap[mid] = obj
            find_menu_daddy(obj.parent_id, menuMap)
            return menuMap


def set_menu(menus, parent_id):
    amenus = [i for i in menus if i.parent_id == parent_id]

    if len(amenus) == 0:
        return []

    nocache = False
    all_menus = []
    for item in amenus:
        menu = {
            'path': item.curl,
            'component': item.code,
            'name': item.code,
            'hidden': item.hidden,
            'meta': {'title': item.code, 'icon': item.icon, 'nocache': nocache},
            'children': []
        }
        if item.type == 3:
            menu['hidden'] = True

        # 查询是否有子级
        menu_children = set_menu(menus, item.id)
        if len(menu_children) > 0:
            menu['children'] = menu_children

        if item.type == 2:
            # 添加子级首页，有这一级NoCache才有效
            menu_index = {
                'path': 'index',
                'component': item.code,
                'name': item.code,
                'meta': {'title': item.code, 'icon': item.icon, 'nocache': nocache},
                'children': []
            }
            menu['children'].append(menu_index)
            menu['meta'] = []

        all_menus.append(menu)
    return all_menus


# 新增菜单后自动添加菜单下的常规操作
def init_menu(menu):
    if menu.type == 2:
        menu_list = [
            {"name": "新增", "code": menu.code + "add", "curl": menu.curl + "/add", 'type': 3, "operate": "add", "sequence": 10, "parent_id": menu.id},
            {"name": "删除", "code": menu.code + "del", "curl": menu.curl + "/del", 'type': 3, "operate": "del", "sequence": 20, "parent_id": menu.id},
            {"name": "编辑", "code": menu.code + "update", "curl": menu.curl + "/update", 'type': 3, "operate": "update", "sequence": 30, "parent_id": menu.id},
            {"name": "查看", "code": menu.code + "view", "curl": menu.curl + "/view", 'type': 3, "operate": "view", "sequence": 40, "parent_id": menu.id},
        ]

        menu_models = []
        for item in menu_list:
            menu_models.append(Menu(name=item['name'], code=item['code'], curl=item['curl'], type=item['type'], operate=item['operate'],
                                    sequence=item['sequence'], parent_id=item['parent_id'], ))
        Menu.objects.bulk_create(menu_models)
