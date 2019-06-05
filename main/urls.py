"""rallyman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url

from .views.home import HomeView
from .views.lobby import LobbyView
from .views.rally import CreateRallyView, ShowRallyView, RemoveRallyView, \
    EditRallyView, EditRallyAddStageView, EditRallyRemoveStageView, EditRallyAddZoneView, \
    RegisterToRallyView, UnRegisterFromRallyView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='main-home'),
    url(r'^lobby', LobbyView.as_view(), name='main-lobby'),

    url(r'^rally$', CreateRallyView.as_view(), name='rally-create'),
    url(r'^rally/(?P<pk>[0-9]+)$', ShowRallyView.as_view(), name='rally-show'),
    url(r'^rally/(?P<pk>[0-9]+)/register', RegisterToRallyView.as_view(), name='rally-register'),
    url(r'^rally/(?P<pk>[0-9]+)/unregister', UnRegisterFromRallyView.as_view(), name='rally-unregister'),

    url(r'^rally/(?P<pk>[0-9]+)/edit/add-stage',
        EditRallyAddStageView.as_view(), name='rally-edit-add-stage'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/remove-stage',
        EditRallyRemoveStageView.as_view(), name='rally-edit-remove-stage'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/stage/(?P<stage_num>[0-9]+)/add-section',
        EditRallyAddZoneView.as_view(), name='rally-edit-add-section'),
    url(r'^rally/(?P<pk>[0-9]+)/edit', EditRallyView.as_view(), name='rally-edit'),
    url(r'^rally/(?P<pk>[0-9]+)/remove', RemoveRallyView.as_view(), name='rally-remove'),
]
