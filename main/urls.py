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

from .views.about import AboutView
from .views.home import HomeView
from .views.lobby import LobbyView
from .views import rally
from .views.rally import edit as rally_edit

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='main-home'),
    url(r'^about', AboutView.as_view(), name='about'),
    url(r'^lobby', LobbyView.as_view(), name='main-lobby'),

    url(r'^rally$', rally.CreateView.as_view(), name='rally-create'),
    url(r'^rally/(?P<pk>[0-9]+)$', rally.ShowView.as_view(), name='rally-show'),
    url(r'^rally/(?P<pk>[0-9]+)/register', rally.RegisterView.as_view(), name='rally-register'),
    url(r'^rally/(?P<pk>[0-9]+)/unregister', rally.UnRegisterView.as_view(), name='rally-unregister'),

    url(r'^rally/(?P<pk>[0-9]+)/edit/add-stage',
        rally_edit.AddStageView.as_view(), name='rally-edit-add-stage'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/remove-stage',
        rally_edit.RemoveStageView.as_view(), name='rally-edit-remove-stage'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/stage/(?P<stage_num>[0-9]+)/add-section',
        rally_edit.AddSectionView.as_view(), name='rally-edit-add-section'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/planning',
        rally_edit.PlanningView.as_view(), name='rally-edit-planning'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/roadbook',
        rally_edit.RoadbookView.as_view(), name='rally-edit-roadbook'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/participants',
        rally_edit.ParticipantsView.as_view(), name='rally-edit-participants'),
    url(r'^rally/(?P<pk>[0-9]+)/edit/participant/position',
        rally_edit.ChangePositionView.as_view(), name='rally-edit-participant-change-position'),
    url(r'^rally/(?P<pk>[0-9]+)/invite/participant',
        rally_edit.InviteView.as_view(), name='rally-invite-participant'),
    url(r'^rally/(?P<pk>[0-9]+)/kick/participant/(?P<uid>[0-9]+)',
        rally_edit.KickView.as_view(), name='rally-kick-participant'),

    url(r'^rally/(?P<pk>[0-9]+)/delete', rally.DeleteView.as_view(), name='rally-delete'),
]
