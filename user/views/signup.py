# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import FormView

from main.core.logger import Log

from ..forms.signup import SignUpForm


class SignUpView(FormView):
    template_name = 'user/signup_form.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        context['ariane'] = ['signup']
        return context

    def form_valid(self, form):
        _l = Log(self)

        try:
            _u = User.objects.get(username=form.cleaned_data.get('username'))
            _msg = 'This login is not available. Please choose another one.'
            messages.add_message(self.request, messages.ERROR, _msg)
            return HttpResponseRedirect(reverse('auth-signup'))

        except User.DoesNotExist:
            _firstName = form.cleaned_data.get('first_name', '')
            _lastName = form.cleaned_data.get('last_name', '')
            if _firstName is None:
                _firstName = ''
            if _lastName is None:
                _lastName = ''

            _user = User(username=form.cleaned_data.get('username'),
                         first_name=_firstName,
                         last_name=_lastName)
            _user.set_password(form.cleaned_data.get('password'))
            _user.save()

            _msg = 'User account created successfully'
            _l.info(_msg)
            messages.add_message(self.request, messages.SUCCESS, _msg)

            login(self.request, _user)
            _msg = 'User logged successfully'
            _l.info(_msg)
            messages.add_message(self.request, messages.SUCCESS, _msg)

            return HttpResponseRedirect(reverse('user-profile'))

    def form_invalid(self, form):
        _l = Log(self)
        _msg = 'Error while creating user account : %s' % form.errors
        _l.info(_msg)
        messages.add_message(self.request, messages.ERROR, mark_safe(_msg))
        return HttpResponseRedirect(reverse('auth-signup'))
