# -*- coding: utf-8 -*-
# author: timor

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from systems.views import UserViewSet, RoleViewSet, MenuViewSet

router.register(r'user', UserViewSet)
router.register(r'role', RoleViewSet)
router.register(r'menu', MenuViewSet)

from tools.views import UploadViewSet, FileUploadViewSet

router.register(r'upload', UploadViewSet)
router.register(r'fileupload', FileUploadViewSet)
