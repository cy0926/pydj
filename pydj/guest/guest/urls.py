"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from sign import views

# 导入sign应用viewes文件

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$', views.index),  # 添加 index/路径配置
    url(r'^login_action/$', views.login_action),  # 添加 /login_action/路径配置
    url(r'^event_manage/$', views.event_manage),  # 添加 /event_manage/路径配置
    url(r'^accounts/login/$', views.index),  # 添加跳转，当用户未登录，直接输入/event_manage/网址的时候，跳转登录页
    url(r'^search_name/$', views.search_name),
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^search_realname/$', views.search_realname),
    url(r'^sign_index/(?P<event_id>[0-9]+)/$', views.sign_index),
    url(r'^sign_index_action/(?P<event_id>[0-9]+)/$', views.sign_index_action),
    url(r'^logout/$', views.logout),  # 添加退出目录的路由
    url(r'^api/', include('sign.urls', namespace="sign")),     # 添加接口基本路径 “/api/”
]
