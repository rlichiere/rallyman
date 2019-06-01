# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from ..core.logger import Log

import logging
logger = logging.getLogger('main_logger')


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

        self.log.infoIndirect(message)
        messages.add_message(request, self.SUCCESS, message)
        return HttpResponseRedirect(reverse(_redirect))

    def redirect_error(self, request, message, redirect=None):
        _redirect = self.log.getRedirect()
        if redirect is not None:
            _redirect = redirect

        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return HttpResponseRedirect(reverse(_redirect))

    def set_context_error(self, request, message, context):
        context['error'] = message
        self.log.error(message)
        messages.add_message(request, self.ERROR, message)
        return context
