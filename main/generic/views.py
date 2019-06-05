# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic import TemplateView

from ..core.const.lobby.rallies import RallyStatus
from ..core.logger import Log
from ..models import Rally


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
        _redirectKwargs = dict()
        if redirect is not None:
            _redirect = redirect
            _redirectKwargs = self.log.getRedirectKwargs()

        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return HttpResponseRedirect(reverse(_redirect, kwargs=_redirectKwargs))

    def set_context_error(self, request, message, context):
        context['error'] = message
        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return context

    def get_object_or_404(self, object_model, object_id):
        try:
            return object_model.objects.get(id=object_id)
        except object_model.DoesNotExist:
            self.log.debugIndirect('Object <%s#%s> not found' % (object_model.__name__, object_id))
            raise Http404


class PageView(ViewHelper, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        _status = [RallyStatus.OPENED, RallyStatus.STARTED]
        _userRallies = Rally.objects.filter(participation__player=self.request.user, status__in=_status)

        # dispatch rallies by status
        _dispatchedRallies = dict()
        for _rally in _userRallies:
            if _rally.status not in _dispatchedRallies:
                _dispatchedRallies[_rally.status] = list()

            if _rally.creator == self.request.user:
                _rally.user_is_creator = True

            _dispatchedRallies[_rally.status].append(_rally)
        context['user_rallies'] = _dispatchedRallies

        # dispatch rallies by status
        _userManagedRallies = Rally.objects.filter(creator=self.request.user)
        _dispatchedManagedRallies = dict()
        for _rally in _userManagedRallies:
            if _rally.status not in _dispatchedManagedRallies:
                _dispatchedManagedRallies[_rally.status] = list()

            if _rally.creator == self.request.user:
                _rally.user_is_creator = True

                _dispatchedManagedRallies[_rally.status].append(_rally)
        context['user_managed_rallies'] = _dispatchedManagedRallies

        return context
