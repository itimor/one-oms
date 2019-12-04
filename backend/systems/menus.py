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
    user_role_list = User.objects.filter(username=user).values('roles')
    user_menu_list = Role.objects.filter(id__in=user_role_list).values('menus')

    menuMap = dict()
    for item in user_menu_list:
        menu_info = Menu.objects.get(id=item['menus'])
        menuMap[menu_info.id] = menu_info

    for item in user_menu_list:
        menu_info = Menu.objects.get(id=item['menus'])
        if menu_info.parent in menuMap:
            continue
        user_menus = find_menu_daddy(menu_info.parent_id, menuMap)
    return list(user_menus.values())


def find_menu_daddy(menuid, menuMap):
    obj = Menu.objects.filter(id=menuid).first()
    if obj:
        mid = obj.id
        if mid not in menuMap:
            menuMap[mid] = obj
            find_menu_daddy(obj.parent_id, menuMap)
            return menuMap


def set_menu(menus, parent_id):
    nocache = False
    all_menus = []
    len(menus)
    for item in menus:
        menu = {
            'path': item.curl,
            'component': item.code,
            'name': item.code,
            'meta': {'title': item.name, 'icon': item.icon, 'nocache': nocache},
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
