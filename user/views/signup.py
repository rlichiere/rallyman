# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import FormView

from ..forms.signup import SignUpForm


class SignUpView(FormView):
    template_name = 'user/signup_form.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        _user = User(username=form.cleaned_data.get('username'),
                     email=form.cleaned_data.get('email'),
                     first_name=form.cleaned_data.get('first_name'),
                     last_name=form.cleaned_data.get('last_name'))
        _user.set_password(form.cleaned_data.get('password'))
        _user.save()

        _msg = 'User account created successfully'
        print _msg
        messages.add_message(self.request, messages.SUCCESS, _msg)

        login(self.request, _user)
        _msg = 'User logged successfully'
        print _msg
        messages.add_message(self.request, messages.SUCCESS, _msg)

        return HttpResponseRedirect(reverse('user-profile'))

    def form_invalid(self, form):
        _msg = 'Error while creating user account : %s' % form.errors
        print _msg
        messages.add_message(self.request, messages.ERROR, mark_safe(_msg))
        return HttpResponseRedirect(reverse('auth-signup'))
