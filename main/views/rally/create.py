# -*- coding: utf-8 -*-
from datetime import datetime as dt
import json
import httplib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render

from ...core.const.lobby.rallies import RallyStatus
from ...generic.views import MainTemplateView
from ...models import Rally
from ...forms.rally import CreateRallyForm


class CreateView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally/create.html'

    def __init__(self, *args, **kwargs):
        super(CreateView, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = dict()
        context['form_create'] = CreateRallyForm(request=self.request)
        context['user'] = _executor

        self.log.endView()
        return render(template_name=self.template_name, context=context, request=self.request)

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        context = dict()

        _form = CreateRallyForm(self.request.POST, request=self.request)
        context['form_create'] = _form

        if not _form.is_valid():
            self.log.info('Form is NOT valid : %s' % _form.errors)
            _respContent = json.dumps({'error': _form.errors})
            return HttpResponse(content=_respContent, content_type='application/json', status=httplib.BAD_REQUEST)

        _rally = Rally(label=_form.cleaned_data.get('label'),
                       creator=_executor,
                       started_at=_form.cleaned_data.get('started_at'))

        if _form.cleaned_data.get('set_opened_at'):
            _openedAt = _form.cleaned_data.get('opened_at')
            _rally.opened_at = _openedAt
            _rally.status = RallyStatus.SCHEDULED
        else:
            _rally.opened_at = dt.now()
            _rally.status = RallyStatus.OPENED

        _rally.save()

        self.log.endView()
        return self.return_success(request=self.request,
                                   message='Rally #%s created : %s' % (_rally.id, _rally.label),
                                   status=httplib.CREATED,
                                   redirect_to=_redirect,
                                   redirect_kwargs={'pk': _rally.id})
