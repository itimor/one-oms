# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from systems.api_views import getuserinfo, getmenubutons

urlpatterns = [
    url(r'^getuserinfo/', getuserinfo.as_view()),
    url(r'^getmenubutons/', getmenubutons.as_view()),
]
