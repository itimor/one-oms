# -*- coding: utf-8 -*-
# author: itimor

from systems.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import exceptions
from django.db.models import Q
from systems.menus import get_menus_by_user

class getuserinfo(APIView):
    """登录"""

    def get(self, request, *args, **kwargs):
        ret = {'code': 1000, 'msg': "成功", 'data':[]}
        try:
            user = request.user
            ret['data'] = get_menus_by_user(user)
        except exceptions as e:
            ret['code'] = 1002
            ret['msg'] = "请求异常"
        return Response(ret)
