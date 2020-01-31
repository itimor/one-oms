# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets, permissions
from systems.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin
from rest_framework.decorators import action
from systems.menus import get_menus_by_user, set_menu
from common import status
from collections import OrderedDict


class UserViewSet(BulkModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username']
    filter_fields = ['username']
    ordering_fields = ['username', 'is_active']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return UserReadSerializer
        return UserSerializer


class RoleViewSet(BulkModelMixin):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return RoleReadSerializer
        return RoleSerializer


class MenuViewSet(BulkModelMixin):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return MenuReadSerializer
        return MenuSerializer


class ApiPermViewSet(BulkModelMixin):
    queryset = ApiPerm.objects.all()
    serializer_class = ApiPermSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id']
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return ApiPermReadSerializer
        return ApiPermSerializer


class AuthViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], url_path='getuserinfo', detail=False)
    def getuserinfo(self, request):
        user = request.user
        user_obj = User.objects.get(username=user)

        data = get_menus_by_user(user)

        if len(data) > 0:
            topmenuid = data[0].parent_id
            if not topmenuid:
                topmenuid = data[0].id

        menus = set_menu(data, topmenuid)

        ip = request.META.get("HTTP_X_FORWARDED_FOR", "")
        if not ip:
            ip = request.META.get('REMOTE_ADDR', "")

        data = {'menus': menus, 'username': user_obj.username, 'avatar': user_obj.avatar, 'memo': user_obj.memo, 'ip': ip}
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    @action(methods=['get'], url_path='getmenubutons', detail=False)
    def getmenubutons(self, request):
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
        data = buttons
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))
