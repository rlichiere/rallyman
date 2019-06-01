# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from ..generic.views import ViewHelper


class HomeView(ViewHelper, TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(HomeView, self).get_context_data(**kwargs)

        self.log.endView()
        return context
