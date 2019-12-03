# -*- coding: utf-8 -*-
# author: timor

from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_auth.views import PasswordChangeView
from django.views.generic.base import TemplateView
from core import settings
from core.routerApi import router
from rest_framework_jwt.views import obtain_jwt_token as jwt_token

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              [
                  url(r'^api/', include(router.urls)),

                  # 用户信息
                  url(r'api/systems/', include(('systems.urls', 'systems'), namespace="systems")),
                  url(r'^api/user/changepasswd/', PasswordChangeView.as_view(), name='changepasswd'),

                  # token认证
                  url(r'^api/jwt-token-auth/', jwt_token, name='rest_framework_token'),
                  url(r'^api/api-token-auth/', include('rest_framework.urls', namespace='rest_framework')),

                  # 静态模板
                  #url(r'', TemplateView.as_view(template_name="index.html")),
              ]
