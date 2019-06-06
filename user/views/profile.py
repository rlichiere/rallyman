# -*- coding: utf-8 -*-
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms.profile import UserProfileForm, UserProfilePasswordChangeForm
from main.generic.views import MainTemplateView


class UserProfileView(LoginRequiredMixin, MainTemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['ariane'] = 'profile'
        context['form_fields'] = UserProfileForm(request=self.request)
        context['form_password'] = UserProfilePasswordChangeForm(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor, 'user-profile')

        if self.request.POST.get('password_change'):
            # user modifies password

            _form = UserProfilePasswordChangeForm(self.request.POST, request=self.request)
            if not _form.is_valid():
                return self.redirect_error(self.request, 'Form is not valid')

            _newPass = _form.cleaned_data.get('password')
            if _newPass != _form.cleaned_data.get('password_check'):
                return self.redirect_error(self.request, 'Passwords are different')

            _executor.set_password(_newPass)
            _executor.save()
            login(request, _executor)
            return self.redirect_success(self.request, 'Password changed')

        # user modifies other fields (email, first_name, last_name)
        _form = UserProfileForm(self.request.POST, request=self.request)
        if not _form.is_valid():
            return self.redirect_error(self.request, 'Form is not valid')

        _pEmail = _form.cleaned_data.get('email')
        if _pEmail != _executor.email:
            _executor.email = _pEmail

        _pFirsName = _form.cleaned_data.get('first_name')
        if _pFirsName != _executor.first_name:
            _executor.first_name = _pFirsName

        _pLastName = _form.cleaned_data.get('last_name')
        if _pLastName != _executor.last_name:
            _executor.last_name = _pLastName

        _executor.save()

        return self.redirect_success(self.request, 'Profile changed')
