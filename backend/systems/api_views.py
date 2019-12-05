# -*- coding: utf-8 -*-
# author: itimor

from systems.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from systems.menus import get_menus_by_user, set_menu


class getuserinfo(APIView):
    """登录"""

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "成功", 'data': []}
        try:
            user = request.user
            user_obj = User.objects.get(username=user)

            data = get_menus_by_user(user)

            if len(data) > 0:
                topmenuid = data[0].parent_id
                if not topmenuid:
                    topmenuid = data[0].id

            menus = set_menu(data, topmenuid)
            ret['data'] = {'menus': menus, 'realname': user_obj.realname, 'avatar': user_obj.avatar}
        except exceptions as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return Response(ret)


class getmenubutons(APIView):
    """登录"""

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "成功", 'data': []}
        try:
            user = request.user
            user_obj = User.objects.get(username=user)
            buttons = []

            if user_obj.is_admin:
                buttons = ['add', 'del', 'update', 'view']
            else:
                menucode = request.GET['menucode']

                match_menu = Menu.objects.get(code=menucode)

                data = get_menus_by_user(user)
                for item in data:
                    if item.parent_id == match_menu.id:
                        buttons.append(item.operate)

            ret['data'] = buttons
        except exceptions as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return Response(ret)
