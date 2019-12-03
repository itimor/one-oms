# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets
from systems.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ['username']
    filter_fields = ['username']
    ordering_fields = ['username']


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    filter_fields = ['name']
    ordering_fields = ['parent_id', 'sequence']
