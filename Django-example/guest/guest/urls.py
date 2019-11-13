"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from sign import views



urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.index),
    path('index/', views.index),
    path('login_action/', views.login_action),
    path('event_manage/', views.event_manage),
    path('accounts/login/', views.index),
    path('search_event_name/', views.search_event_name),
    # path('search_guest_phone/', views.search_guest_phone),
    path('guest_manage/', views.guest_manage),
    re_path('sign_index/(?P<eid>[0-9]+)/$', views.sign_index),
    re_path('sign_index_action/(?P<eid>[0-9]+)/$', views.sign_index_action),
    path('logout/', views.logout),
    path('api/', include('sign.urls', namespace="sign")),
]
