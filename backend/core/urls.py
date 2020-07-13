# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic.base import TemplateView
from core import settings
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              [
                  # django管理后台
                  url(r'^admin/', admin.site.urls),
                  # 工具管理
                  url(r'api/tool/', include(('tools.urls', 'tools'), namespace="tools")),
                  # 系统管理
                  url(r'api/sys/', include(('systems.urls', 'systems'), namespace="systems")),
                  # 通知管理
                  url(r'api/notice/', include(('notices.urls', 'notices'), namespace="notices")),
              ]

if settings.APP_ENV == 'prod':
    from rest_framework.documentation import include_docs_urls

    urlpatterns += [
        # api文档
        url(r'^docs/', include_docs_urls(title='X Document')),
        # 静态模板
        url(r'', TemplateView.as_view(template_name="index.html")),
    ]
