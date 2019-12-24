# -*- coding: utf-8 -*-
# author: timor

from workflows.models import *
from systems.models import User
from rest_framework import serializers
from utils.index import create_time_pid

class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = '__all__'


class WorkflowStepSerializer(serializers.ModelSerializer):
    action_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = WorkflowStep
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    workflow = serializers.SlugRelatedField(queryset=Workflow.objects.all(), slug_field='name')
    create_user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Ticket
        fields = '__all__'
        extra_kwargs = {'pid': {'required': False}}

    def create(self, validated_data):
        obj = Ticket.objects.create(**validated_data)
        p = create_time_pid()
        obj.pid = '{}{}'.format(p, obj.id)
        obj.save()
        return obj


class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = '__all__'
