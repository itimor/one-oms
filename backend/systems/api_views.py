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
            menu_data = get_menus_by_user(user)

            if len(menu_data) > 0:
                topmenuid = menu_data[0].parent_id
                if topmenuid == 0:
                    topmenuid = menu_data[0].id
            menus = set_menu(menu_data, topmenuid)
            print(menus)
            ret['data'] = {'menus': menus, 'realname': user_obj.realname, 'avatar': user_obj.avatar}
        except exceptions as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return Response(ret)
