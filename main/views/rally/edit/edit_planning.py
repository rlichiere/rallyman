# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied
from django.utils.safestring import mark_safe

from ....core.const.lobby.rallies import RallyStatus
from ....generic.views import MainTemplateView
from ....models import Rally
from ....forms.rally import EditRallyPlanningForm


class PlanningView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_edit_planning.html'

    def __init__(self, *args, **kwargs):
        super(PlanningView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})
        context = super(PlanningView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, self.kwargs['pk'])

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['ariane'] = ['edit_rally', 'planning']
        context['rally'] = _rally
        context['planning_is_editable'] = bool(_rally.status in [RallyStatus.SCHEDULED])
        context['form_planning'] = EditRallyPlanningForm(request=self.request, rally=_rally)
        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rally = self.get_object_or_404(Rally, kwargs.get('pk'))

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _form = EditRallyPlanningForm(self.request.POST, request=self.request, rally=_rally)
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid: %s' % _form.errors))

        _form.execute()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally planning edited successfully')
