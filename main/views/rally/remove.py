# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin

from ...generic.views import MainTemplateView
from ...models import Rally


class RemoveRallyView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_create.html'

    def __init__(self, *args, **kwargs):
        super(RemoveRallyView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        # check permissions

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)
        _rally.delete()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally removed successfully')
