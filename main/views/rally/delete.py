# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied

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

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['rally'] = _rally

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _redirect = self.request.GET.get('redirect', 'main-home')
        _rallyId = kwargs.get('pk')
        self.log.startView(_executor, _redirect)

        _rally = self.get_object_or_404(Rally, _rallyId)

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)
        _rally.delete()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally deleted successfully')
