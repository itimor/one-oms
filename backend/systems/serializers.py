# -*- coding: utf-8 -*-
# author: timor

from systems.models import *
from rest_framework import serializers
from systems.menus import init_menu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        roles = validated_data.pop('roles')
        obj = User.objects.create(**validated_data)
        obj.roles.set(roles)
        try:
            obj.set_password(validated_data['password'])
        except:
            pass
        obj.save()
        return obj

    def update(self, instance, validated_data):
        roles = validated_data.pop('roles')
        instance.username = validated_data.get('username', instance.username)
        instance.realname = validated_data.get('realname', instance.realname)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.memo = validated_data.get('memo', instance.memo)
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

    def create(self, validated_data):
        obj = Menu.objects.create(**validated_data)
        if obj.type == 2:
            init_menu(obj)
        return obj
