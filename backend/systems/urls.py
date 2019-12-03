# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from systems.api_views import getuserinfo

urlpatterns = [
    url(r'^getuserinfo/', getuserinfo.as_view()),
]
