# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth import password_validation as django_password_validators
from django.contrib.auth import validators as auth_validators
from django.contrib.auth.models import User

from rallyman import settings

from main.core import config
from main.core.const import user as const_user

from user.validators import password_validation


class SignUpForm(forms.Form):
    username = forms.CharField(label='Login',
                               help_text='Enter a username to log in.<br />'
                                         ' It will never be shown to other people')
    password = forms.CharField(label='Password',
                               help_text='Enter a password to log in.<br />'
                                         ' It will be stored in our database in an encrypted form,'
                                         ' with no possibility of retrieving its value in plain text.',
                               widget=PasswordInput())
    password_confirmation = forms.CharField(label='Password confirmation',
                                            help_text='Enter your password a second time to ensure the provided value',
                                            widget=PasswordInput())
    first_name = forms.CharField(label='First name',
                                 help_text='Enter your first name.<br />'
                                           ' This value is used in conjunction with your last name'
                                           ' to identify you to others. You can use a pseudo instead of your real name',
                                 required=False,
                                 initial='')
    last_name = forms.CharField(label='Last name',
                                help_text='Enter your last name.<br />'
                                          ' This value is used in conjunction with your first name'
                                          ' to identify you to others. You can use a pseudo instead of your real name',
                                required=False,
                                initial='')

    def __init__(self, **kwargs):
        super(SignUpForm, self).__init__(**kwargs)

        for _fieldName, _field in self.fields.iteritems():
            self.initializeField(_fieldName, _field)

    def clean_password(self):
        _password = str(self.cleaned_data['password'])

        if len(_password) < self.fields['password'].min_length:
            raise forms.ValidationError('The password in not long enough')

        if len(_password) > self.fields['password'].max_length:
            raise forms.ValidationError('The password is too long')

        # check that password respect complexity rules
        django_password_validators.validate_password(_password)

        return _password

    def clean_password_confirmation(self):
        _passwordConfirmation = str(self.cleaned_data['password_confirmation'])

        # check that password respect complexity rules
        django_password_validators.validate_password(_passwordConfirmation)

        _password = self.cleaned_data.get('password')
        # check that both passwords are identical
        if _password is None:
            if (_password is not None) and (_password != _passwordConfirmation):
                raise forms.ValidationError('The two password fields did not match')

        return _passwordConfirmation

    def clean_first_name(self):
        _firstName = self.cleaned_data['first_name']

        if len(_firstName) < self.fields['first_name'].min_length:
            raise forms.ValidationError('The first name is not long enough')

        if len(_firstName) > self.fields['first_name'].max_length:
            raise forms.ValidationError('The first name is too long')

        return _firstName

    def clean_last_name(self):
        _lastName = self.cleaned_data['last_name']

        if len(_lastName) < self.fields['last_name'].min_length:
            raise forms.ValidationError('The last name is not long enough')

        if len(_lastName) > self.fields['last_name'].max_length:
            raise forms.ValidationError('The last name is too long')

        _firstName = self.cleaned_data.get('first_name')
        if _firstName is not None:
            if (_firstName == '') and (_lastName == ''):
                raise forms.ValidationError('You must fill in at least one of the following fields: First name, Last name')

        return _lastName

    def initializeField(self, field_name, field):

        # prepare data structure
        _helpTextData = {
            'intro': self.fields[field_name].help_text,
            'format': '',
            'constraints': [],
        }

        # initialize field mix/max
        _modelsFieldsNames = [f.name for f in User._meta.get_fields()]
        if field_name in _modelsFieldsNames:
            _minConst = getattr(const_user, '%s__MIN_LENGTH' % field_name.upper())
            _maxConst = getattr(const_user, '%s__MAX_LENGTH' % field_name.upper())
            _minLength = config.get_config('user/%s/min_length' % field_name, _minConst)
            _maxLength = config.get_config('user/%s/max_length' % field_name, _maxConst)
            self.fields[field_name].min_length = _minLength
            self.fields[field_name].max_length = _maxLength

            # manage special case for password field
            if field_name == 'password':
                settings.AUTH_PASSWORD_VALIDATORS[1]['OPTIONS']['min_length'] = _minLength

            # add min/max constraints
            _msg = 'This value must contain from %s to %s characters' % (_minLength, _maxLength)
            _helpTextData['constraints'].append(_msg)

        # manage special case for password field
        if field_name == 'password':
            _passwordValidators = [
                django_password_validators.UserAttributeSimilarityValidator(),
                django_password_validators.CommonPasswordValidator(),
                django_password_validators.NumericPasswordValidator(),
                password_validation.ComplexPasswordValidator()
            ]
            for _validator in _passwordValidators:
                _helpTextData['constraints'].append(_validator.get_help_text())

        # add help_text from the validators of the corresponding model field
        if field_name in _modelsFieldsNames:
            for _validator in User._meta.get_field(field_name).validators:

                _validatorMessage = _validator.message
                if _validatorMessage == '':
                    continue

                # manage special case: detect and remove a superfluous know text
                if type(_validator) is auth_validators.ASCIIUsernameValidator:
                    _textToRemove = 'Enter a valid username. '
                    _index = _validatorMessage.find(_textToRemove)
                    if _index == 0:
                        _validatorMessage = _validatorMessage[len(_textToRemove):]

                _helpTextData['constraints'].append(_validatorMessage)

        # replace initial <str>:help_text by <dict>:help text data
        self.fields[field_name].help_text = _helpTextData
