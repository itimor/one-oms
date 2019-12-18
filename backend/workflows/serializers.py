# -*- coding: utf-8 -*-
# author: timor

from workflows.models import *
from systems.models import User
from rest_framework import serializers


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

    class Meta:
        model = Ticket
        fields = '__all__'


class TicketReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReply
        fields = '__all__'
