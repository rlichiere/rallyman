# -*- coding: utf-8 -*-
from datetime import datetime as dt

from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from ...core.const.lobby.rallies import RallyStatus
from ...generic.views import ViewHelper
from ...models import Rally
from ...forms.rally import CreateRallyForm


class CreateRallyView(ViewHelper, TemplateView):
    template_name = 'main/rally_create.html'

    def __init__(self, *args, **kwargs):
        super(CreateRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(CreateRallyView, self).get_context_data(**kwargs)
        context['form_create'] = CreateRallyForm(request=self.request)

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        _now = dt.now()

        _form = CreateRallyForm(self.request.POST, request=self.request)
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid : %s' % _form.errors))

        _rally = Rally(label=_form.cleaned_data.get('label'), creator=_executor)

        if _form.cleaned_data.get('set_opened_at'):
            _openedAt = _form.cleaned_data.get('opened_at')
            _rally.opened_at = _openedAt
            _rally.status = RallyStatus.SCHEDULED
        else:
            _rally.opened_at = _now
            _rally.status = RallyStatus.OPENED
        _rally.save()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally created successfully')
