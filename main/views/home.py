# -*- coding: utf-8 -*-
from ..generic.views import MainTemplateView


class HomeView(MainTemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(HomeView, self).get_context_data(**kwargs)
        context['ariane'] = ['home']

        self.log.endView()
        return context
