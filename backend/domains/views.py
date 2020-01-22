# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets, permissions
from domains.serializers import *
from common.views import ModelViewSet, FKModelViewSet, JsonResponse, BulkModelMixin


class CDNViewSet(BulkModelMixin):
    queryset = CDN.objects.all()
    serializer_class = CDNSerializer
    search_fields = ['name', 'code']
    filter_fields = ['name', 'code']
    ordering_fields = ['code']


class IPPoolViewSet(BulkModelMixin):
    queryset = IPPool.objects.all()
    serializer_class = IPPoolSerializer
    search_fields = ['ip']
    filter_fields = ['ip']
    ordering_fields = ['ip']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return IPPoolReadSerializer
        return IPPoolSerializer


class ProjectViewSet(BulkModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    search_fields = ['name']
    filter_fields = ['name', 'status']
    ordering_fields = ['status']


class DomainViewSet(BulkModelMixin):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    search_fields = ['domain']
    filter_fields = ['project', 'type']
    ordering_fields = ['brand']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return DomainReadSerializer
        return DomainSerializer
