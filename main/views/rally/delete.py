# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin

from ...generic.views import MainTemplateView
from ...models import Rally


class DeleteRallyView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_delete.html'

    def __init__(self, *args, **kwargs):
        super(DeleteRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)
        context = super(DeleteRallyView, self).get_context_data(**kwargs)

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)
        context['rally'] = _rally

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        # check permissions

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)
        _rally.delete()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally deleted successfully')
