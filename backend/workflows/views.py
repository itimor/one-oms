# -*- coding: utf-8 -*-
# author: timor

from rest_framework import viewsets
from workflows.serializers import *


class WorkflowViewSet(viewsets.ModelViewSet):
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    search_fields = ['name']
    filter_fields = ['name']
    ordering_fields = ['name', 'status']


class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    search_fields = ['name']
    filter_fields = ['name', 'sequence', 'workflow_id']
    ordering_fields = ['sequence']


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    search_fields = ['name']
    filter_fields = ['pid', 'name', 'status']
    ordering_fields = ['status', 'create_time']


class TicketReplyViewSet(viewsets.ModelViewSet):
    queryset = TicketReply.objects.all()
    serializer_class = TicketReplySerializer
    search_fields = ['ticket']
    filter_fields = ['ticket']
    ordering_fields = ['status', '-create_time']
