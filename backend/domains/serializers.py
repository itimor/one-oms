# -*- coding: utf-8 -*-
# author: timor

from domains.models import *
from rest_framework import serializers

class CDNSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDN
        fields = '__all__'


class IPPoolReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPPool
        fields = '__all__'
        depth = 1


class IPPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPPool
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class DomainReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
        depth = 1


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
