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
    allmenus = Menu.objects.all()
    user_role_list = User.objects.filter(username=user).values('roles')
    user_menu_list = Role.objects.filter(id__in=user_role_list).values('menus')
    user_all_menu = dict()
    nocache = False

    menuMapAll = {}
    menuMap = {}
    for item in allmenus:
        menuMapAll[item.id] = item

    for item in user_menu_list:
        menu_info = Menu.objects.get(id=item['menus'])
        # menu = {
        #     'path': menu_info.curl,
        #     'component': menu_info.code,
        #     'name': menu_info.code,
        #     'meta': {'title': menu_info.name, 'icon': menu_info.icon, 'nocache': nocache},
        #     'children': []
        # }
        menuMap[menu_info.id] = menu_info

    for item in user_menu_list:
        menu_info = Menu.objects.get(id=item['menus'])
        if menu_info.parent in menuMap:
            continue
        aaa = setMenuUp(menuMapAll, menu_info.parent, menuMap)
        print(aaa)

    return aaa

def setMenuUp(menuMapAll, menuid, menuMap):
    if menuid in menuMapAll:
        mid = menuMapAll[menuid].id
        print(mid)
        if mid not in menuMap:
            menuMap[mid] = menuMapAll[menuid]
            return setMenuUp(menuMapAll, menuMapAll[menuid].parent, menuMap)
        else:
            return menuMap
