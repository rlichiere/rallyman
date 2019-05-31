# -*- coding: utf-8 -*-
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView


class GenericTemplateView(TemplateView):
    def __init__(self, *args, **kwargs):
        super(GenericTemplateView, self).__init__(*args, **kwargs)


class GenericFormView(FormView):
    def __init__(self, *args, **kwargs):
        super(GenericFormView, self).__init__(*args, **kwargs)


class ViewHelper(object):
    SUCCESS = messages.SUCCESS
    ERROR = messages.ERROR

    def __init__(self, *args, **kwargs):
        _lp = '%s.__init__:' % self.__class__.__name__

        for _arg in args:
            print '%s arg : %s' % (_lp, _arg)

        for _k, _v in kwargs.iteritems():
            print '%s k : %s, v : %s' % (_lp, _k, _v)

    @staticmethod
    def add_message(request, status, message):
        print message
        messages.add_message(request, status, message)

    @classmethod
    def return_error(cls, request, message, target):
        print message
        messages.add_message(request, cls.ERROR, message)
        return HttpResponseRedirect(reverse(target))

    @classmethod
    def set_context_error(cls, request, message, context):
        context['error'] = message
        print message
        messages.add_message(request, cls.ERROR, message)
        return context

    @classmethod
    def return_success(cls, request, message, target):
        print message
        messages.add_message(request, cls.SUCCESS, message)
        return HttpResponseRedirect(reverse(target))
