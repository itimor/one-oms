# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url, include
from rest_framework import routers
from rest_auth.views import PasswordChangeView
from rest_framework_jwt.views import obtain_jwt_token as jwt_token
from systems.views import UserViewSet, RoleViewSet, MenuViewSet, ApiPermViewSet, AuthViewSet

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'role', RoleViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'apiperm', ApiPermViewSet)
router.register(r'auth', AuthViewSet)

urlpatterns = [
    url(r'^auth/changepwd/', PasswordChangeView.as_view(), name='changepwd'),
    # token认证
    url(r'^auth/jwt-token-auth/', jwt_token, name='rest_framework_token'),
    url(r'^auth/api-token-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls
