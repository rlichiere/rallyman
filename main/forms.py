# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput

from .core import constants


class SignInForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=PasswordInput())


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=512)
    first_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200, required=False)


class UserProfileForm(forms.Form):
    email = forms.EmailField(max_length=512)
    first_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200, required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        _executor = request.user

        super(UserProfileForm, self).__init__(*args, **kwargs)
        if len(request.POST) == 0:
            self.fields['email'].initial = _executor.email
            self.fields['first_name'].initial = _executor.first_name
            self.fields['last_name'].initial = _executor.last_name


class UserProfilePasswordChangeForm(forms.Form):
    password_change = forms.BooleanField(initial=True)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserProfilePasswordChangeForm, self).__init__(*args, **kwargs)


class FilterGamesForm(forms.Form):
    user_participation = forms.ChoiceField(choices=[('', '---'), ('True', 'Yes'), ('False', 'No')], required=False)
    game_status = forms.ChoiceField(choices=constants.GameStatus.as_choices_with_undefined(), required=False)
    game_creator = forms.ChoiceField(choices=[('', '---'), ('me', 'Me'), ('notme', 'Not me')], required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(FilterGamesForm, self).__init__(*args, **kwargs)

        self.fields['user_participation'].initial = request.GET.get('user_participation', '')
        self.fields['game_status'].initial = request.GET.get('game_status', '')
        self.fields['game_creator'].initial = request.GET.get('game_creator', '')
