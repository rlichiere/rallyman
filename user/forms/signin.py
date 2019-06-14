# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput


class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=PasswordInput())
