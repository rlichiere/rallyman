# -*- coding: utf-8 -*-
from ...generic.views import PageView
from ...models import Rally


class ShowRallyView(PageView):
    template_name = 'main/rally_show.html'

    def __init__(self, *args, **kwargs):
        super(ShowRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(ShowRallyView, self).get_context_data(**kwargs)
        context['ariane'] = 'show_rally'
        _rally = self.get_object_or_404(Rally, kwargs.get('pk'))
        context['rally'] = _rally

        self.log.endView()
        return context
