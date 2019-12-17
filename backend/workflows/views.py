# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets
from systems.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username']
    filter_fields = ['username']
    ordering_fields = ['username', 'is_active']


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']
