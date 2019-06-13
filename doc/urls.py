# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^doc$', views.DocPageView.as_view(), name='doc'),
    url(r'^doc/(?P<pk>[a-z0-9-_]+)$', views.DocPageView.as_view(), name='doc-page'),
]
