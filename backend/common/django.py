# -*- coding: utf-8 -*-
# author: timor

from django.utils.deprecation import MiddlewareMixin
from rest_framework.pagination import LimitOffsetPagination


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)


class CustomLimitOffsetPagination(LimitOffsetPagination):
    def get_offset(self, request):
        try:
            return (int(request.query_params['offset']) - 1) * int(request.query_params['limit'])
        except (KeyError, ValueError):
            return 1
