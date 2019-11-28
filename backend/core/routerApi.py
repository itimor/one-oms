# -*- coding: utf-8 -*-
# author: timor

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

from systems.views import UserViewSet, RoleViewSet, MenuViewSet

router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'menus', MenuViewSet)

from tools.views import UploadViewSet, FileUploadViewSet

router.register(r'uploads', UploadViewSet)
router.register(r'fileuploads', FileUploadViewSet)
