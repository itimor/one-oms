# -*- coding: utf-8 -*-
# author: itimor

from systems.models import *


def getSuperAdminMenu():
    menuTop = {
        'path': "/sys",
        'component': "Sys",
        'name': "Sys",
        'meta': {'title': "系统管理", 'icon': 'sys', 'nocache': False},
        'children': []
    }
    userPage = {
        'path': "/user",
        'component': "user",
        'name': "user",
        'meta': {'title': "用户管理", 'icon': 'user', 'nocache': False},
        'children': []
    }
    rolePage = {
        'path': "/menu",
        'component': "role",
        'name': "role",
        'meta': {'title': "角色管理", 'icon': 'role', 'nocache': False},
        'children': []
    }
    menuPage = {
        'path': "/menu",
        'component': "menu",
        'name': "menu",
        'meta': {'title': "菜单管理", 'icon': 'menu', 'nocache': False},
        'children': []
    }
    menuTop['children'] = [userPage, rolePage, menuPage]
    return menuTop


# 获取菜单有权限的操作列表

# 获取管理员权限下所有菜单
def get_menus_by_user(user):
    user_obj = User.objects.get(username=user)

    if user_obj.is_admin:
        menus = Menu.objects.all()
        if len(menus) == 0:
            topmenu = Menu.objects.create(name='top',code='top',curl='/top',icon='top',sequence=0)
            menu_list = [
                {
                    "id": 2,
                    "name": "系统管理",
                    "code": "sys",
                    "curl": "/sys",
                    "icon": "1",
                    "hidden": false,
                    "affix": true,
                    "sequence": 1,
                    "type": "1",
                    "status": "1",
                    "operate": "none",
                    "desc": "",
                    "parent": 1
                },
                {
                    "id": 3,
                    "name": "用户管理",
                    "code": "user",
                    "curl": "/user",
                    "icon": "1",
                    "hidden": false,
                    "affix": true,
                    "sequence": 10,
                    "type": "2",
                    "status": "1",
                    "operate": "none",
                    "desc": "",
                    "parent": 2
                },
                {
                    "id": 4,
                    "name": "增加用户",
                    "code": "add",
                    "curl": "/add",
                    "icon": "1",
                    "hidden": false,
                    "affix": true,
                    "sequence": 110,
                    "type": "3",
                    "status": "1",
                    "operate": "add",
                    "desc": "",
                    "parent": 3
                },
                {
                    "id": 5,
                    "name": "角色管理",
                    "code": "role",
                    "curl": "/role",
                    "icon": "role",
                    "hidden": false,
                    "affix": true,
                    "sequence": 20,
                    "type": "2",
                    "status": "1",
                    "operate": "none",
                    "desc": "",
                    "parent": 2
                }]
            menu_list.append()
            Menu.objects.bulk_create(menu_list)
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
            'meta': {'title': item.name, 'icon': item.icon, 'nocache': nocache, 'affix': item.affix},
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
                'meta': {'title': item.name, 'icon': item.icon, 'nocache': nocache},
                'children': []
            }
            menu['children'].append(menu_index)
            menu['meta'] = []

        all_menus.append(menu)
    return all_menus
