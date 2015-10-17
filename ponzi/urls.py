from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    'ponzi.views',
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.add, name='add'),
    url(r'^list/$', views.addr_list, name='addr_list'),
    url(r'^callback/$', views.callback, name='callback'),
    )
