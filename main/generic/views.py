# -*- coding: utf-8 -*-
import httplib

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import TemplateView, View

from ..core.logger import Log


class ViewHelper(object):
    SUCCESS = messages.SUCCESS
    ERROR = messages.ERROR

    def __init__(self, *args, **kwargs):
        self.log = Log(caller=self)

    def add_message(self, request, status, message):
        self.log.info(message)
        messages.add_message(request, status, message)

    def redirect_success(self, request, message, redirect=None):
        _redirect = self.log.getRedirect()

        if redirect is not None:
            _redirect = redirect

        _redirectKwargs = self.log.getRedirectKwargs()
        if _redirectKwargs is None:
            _redirectKwargs = dict()

        self.log.infoIndirect(message)
        messages.add_message(request, self.SUCCESS, message)
        return HttpResponseRedirect(reverse(_redirect, kwargs=_redirectKwargs))

    def redirect_error(self, request, message, redirect=None):
        _redirect = self.log.getRedirect()

        if redirect is not None:
            _redirect = redirect

        _redirectKwargs = self.log.getRedirectKwargs()
        if _redirectKwargs is None:
            _redirectKwargs = dict()

        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return HttpResponseRedirect(reverse(_redirect, kwargs=_redirectKwargs))

    def set_context_error(self, request, message, context):
        context['error'] = message
        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return context

    def return_success(self, request, message, status=None, redirect_to=None, redirect_kwargs=None):
        _status = httplib.OK if status is None else status
        self.log.infoIndirect(message)
        messages.add_message(request, self.SUCCESS, message)

        _redirectTo = 'main-home'
        _redirectKwargs = {}
        if redirect_to:
            _redirectTo = redirect_to

            if redirect_kwargs:
                _redirectKwargs = redirect_kwargs

        if _redirectTo.find('?') >= 0:
            _viewName, _params = _redirectTo.rsplit('?', 1)
        else:
            _viewName = _redirectTo
            _params = ''

        _callbackUrl = reverse(_viewName, kwargs=_redirectKwargs)
        _callbackUrl += _params
        return HttpResponse(content=_callbackUrl, status=_status)

    def get_object_or_404(self, object_model, object_id):
        try:
            return object_model.objects.get(id=object_id)
        except object_model.DoesNotExist:
            self.log.debugIndirect('Object <%s#%s> not found' % (object_model.__name__, object_id))
            raise Http404


class MainView(ViewHelper, View):
    pass


class MainTemplateView(ViewHelper, TemplateView):
    pass
