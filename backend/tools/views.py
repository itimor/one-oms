# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets
from tools.models import Upload, FileUpload
from tools.serializers import UploadSerializer, FileUploadSerializer
from rest_framework.permissions import AllowAny


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all().order_by("-create_time")
    serializer_class = UploadSerializer
    filter_fields = ('username', 'type',)


class FileUploadViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
