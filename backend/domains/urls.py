# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from domains.views import CDNViewSet, IPPoolViewSet, ProjectViewSet, DomainViewSet


router = routers.DefaultRouter()

router.register(r'cdn', CDNViewSet)
router.register(r'ipool', IPPoolViewSet)
router.register(r'project', ProjectViewSet)
router.register(r'domain', DomainViewSet)

urlpatterns = [
]

urlpatterns += router.urls
