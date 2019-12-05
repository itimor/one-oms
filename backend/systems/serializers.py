# -*- coding: utf-8 -*-
# author: timor

from systems.models import *
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'realname', 'avatar', 'roles', 'is_active', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        user = User.objects.create(**validated_data)
        user.roles.set(roles)
        try:
            user.set_password(validated_data['password'])
        except:
            pass
        user.save()
        return user

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles')
        instance.username = validated_data.get('username', instance.username)
        instance.realname = validated_data.get('realname', instance.realname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        try:
            instance.set_password(validated_data['password'])
        except:
            pass
        instance.roles.set(roles)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
