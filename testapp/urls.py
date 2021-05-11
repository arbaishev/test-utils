# coding=utf-8
# future
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'test/', views.TestView.as_view()),
]

app_name = 'testapp'