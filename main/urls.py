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
from .views.rally.create import CreateRallyView
from .views.rally.register import RegisterToRallyView, UnRegisterFromRallyView


urlpatterns = [
    url(r'^$', HomeView.as_view(), name='main-home'),
    url(r'^lobby', LobbyView.as_view(), name='main-lobby'),
    url(r'^rally/(?P<pk>[0-9]+)/register', RegisterToRallyView.as_view(), name='rally-register'),
    url(r'^rally/(?P<pk>[0-9]+)/unregister', UnRegisterFromRallyView.as_view(), name='rally-unregister'),
    url(r'^rally', CreateRallyView.as_view(), name='rally-create'),
]
