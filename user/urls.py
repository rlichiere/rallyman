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
from django.contrib.auth import views as auth_views

from .forms.signin import SignInForm
from .views.signup import SignUpView
from .views.profile import UserProfileView


urlpatterns = [
    url(r'^signup', SignUpView.as_view(), name='auth-signup'),
    url(r'^signin', auth_views.login, {'template_name': 'user/signin.html',
                                       'authentication_form': SignInForm}, name='auth-signin'),
    url(r'^signout', auth_views.logout, {'next_page': '/signin'}, name='auth-signout'),
    url(r'^user/profile', UserProfileView.as_view(), name='user-profile'),
]
