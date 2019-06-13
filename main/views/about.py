# -*- coding: utf-8 -*-
from ..generic.views import MainTemplateView

from rallyman.version import version

from ..core.const import copyright


class AboutView(MainTemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(AboutView, self).get_context_data(**kwargs)

        context['version'] = version
        context['copyright'] = copyright

        self.log.endView()
        return context
