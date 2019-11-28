# -*- coding: utf-8 -*-
# author: timor

from rest_framework import serializers
from tools.models import Upload, FileUpload


class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['url', 'id', 'username', 'file', 'filename', 'filepath', 'archive', 'type', 'size', 'create_time']


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['url', 'id', 'file']
