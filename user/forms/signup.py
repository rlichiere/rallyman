# -*- coding: utf-8 -*-
from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=512)
    first_name = forms.CharField(max_length=200, required=False)
    last_name = forms.CharField(max_length=200, required=False)
