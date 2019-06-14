# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth import password_validation


class SignUpForm(forms.Form):
    username = forms.CharField(label='Login',
                               max_length=200)
    password = forms.CharField(help_text='CUSTOM help text !!!',
                               label='Password',
                               min_length=12,
                               max_length=200,
                               widget=PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation',
                                            min_length=12,
                                            max_length=200,
                                            widget=PasswordInput())
    first_name = forms.CharField(label='First name',
                                 max_length=200,
                                 required=False,
                                 initial='')
    last_name = forms.CharField(label='Last name',
                                max_length=200,
                                required=False,
                                initial='')

    def clean_password_confirmation(self):

        _password = str(self.cleaned_data['password'])
        _passwordConfirmation = str(self.cleaned_data['password_confirmation'])

        # check that both passwords are identical
        if _password != _passwordConfirmation:
            raise forms.ValidationError('The two password fields did not match.')

        # check that password respect complexity rules
        password_validation.validate_password(_password)
        password_validation.validate_password(_passwordConfirmation)

        return True

    def clean_last_name(self):
        _firstName = self.cleaned_data['first_name']
        _lastName = self.cleaned_data['last_name']

        if (_firstName == '') and (_lastName == ''):
            raise forms.ValidationError('You must fill in at least one of the following fields: First name, Last name')

        return _lastName
