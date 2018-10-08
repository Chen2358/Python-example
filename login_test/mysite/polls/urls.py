from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^show_login$', views.show_login, name='show_login'),
    url(r'^date$', views.date, name='date'),
]