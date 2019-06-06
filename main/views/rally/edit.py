# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, View

from ...core.const.lobby.rallies import RallyStatus
from ...generic.views import ViewHelper, PageTemplateView
from ...models import Rally, Stage
from ...forms.rally import EditRallyStagesForm


class EditRallyView(LoginRequiredMixin, PageTemplateView):
    template_name = 'main/rally_edit.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})
        context = super(EditRallyView, self).get_context_data(**kwargs)

        # check permissions

        context['ariane'] = 'edit_rally'
        _rally = self.get_object_or_404(Rally, self.kwargs['pk'])
        context['rally'] = _rally
        if _rally.status not in [RallyStatus.SCHEDULED, RallyStatus.OPENED]:
            return self.set_context_error(self.request, 'This rally cannot be edited due to its status : %s' % _rally.status, context)

        _stages = Stage.objects.filter(rally=_rally.id)
        _stagesData = list()
        for _stage in Stage.objects.filter(rally=_rally.id):
            _stageData = dict()
            _stageData['sections'] = _stage.get_roadbook
            _stageData['number_of_sections'] = len(_stageData['sections'])

            _stagesData.append(_stageData)

        context['stages'] = _stagesData
        context['stages_count'] = _stages.count() if _stages.count() > 0 else 1

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rally = self.get_object_or_404(Rally, kwargs.get('pk'))

        _form = EditRallyStagesForm(self.request.POST, request=self.request, rally=_rally)
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid : %s' % _form.errors))

        _form.execute()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally stages edited successfully')


class EditRallyAddStageView(LoginRequiredMixin, PageTemplateView):
    template_name = 'main/rally_edit_stage.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyAddStageView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(EditRallyAddStageView, self).get_context_data(**kwargs)
        context['rally'] = self.get_object_or_404(Rally, self.kwargs['pk'])
        context['stage_num'] = self.request.GET.get('stage_num')

        self.log.endView()
        return context


class EditRallyRemoveStageView(LoginRequiredMixin, ViewHelper, View):
    template_name = 'main/rally_edit_stage.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyRemoveStageView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)

        _stageNum = self.request.POST['stage_num']

        _stages = Stage.objects.filter(rally=_rally).order_by('position_in_roadbook').order_by('position_in_roadbook')
        _stageIdx = 0
        _stageFound = False
        for _stage in _stages:
            _stageIdx += 1

            if _stageIdx == int(_stageNum):
                _stage.delete()
                _stageFound = True
                continue

            if _stageFound:
                _stage.position_in_roadbook = _stage.position_in_roadbook - 1
                _stage.save()

        if not _stageFound:
            return self.redirect_error(self.request, 'Stage %s not found for rally %s' % (_stageNum, _rallyId))

        self.log.endView()
        return self.redirect_success(self.request, 'Rally stage %s removed successfully from rally %s' % (_stageNum, _rallyId))


class EditRallyAddZoneView(LoginRequiredMixin, PageTemplateView):
    template_name = 'main/rally_edit_stage_section.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyAddZoneView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(EditRallyAddZoneView, self).get_context_data(**kwargs)
        context['stage_num'] = kwargs.get('stage_num')
        context['section_num'] = self.request.GET.get('section_num')

        self.log.endView()
        return context
