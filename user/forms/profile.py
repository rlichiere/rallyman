# -*- coding: utf-8 -*-
from django import forms


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
        request = kwargs.pop('request')
        super(UserProfilePasswordChangeForm, self).__init__(*args, **kwargs)
