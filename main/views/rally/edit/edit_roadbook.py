# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied
from django.utils.safestring import mark_safe

from ....core.const.lobby.rallies import RallyStatus
from ....generic.views import MainTemplateView, MainView
from ....models import Rally, Stage
from ....forms.rally import EditRallyStagesForm


class RoadbookView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally/edit/roadbook.html'

    def __init__(self, *args, **kwargs):
        super(RoadbookView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})
        context = super(RoadbookView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, self.kwargs['pk'])

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['ariane'] = ['edit_rally', 'roadbook']
        context['rally'] = _rally
        if _rally.status not in [RallyStatus.SCHEDULED, RallyStatus.OPENED]:
            _msg = 'This rally cannot be edited due to its status : %s' % _rally.status
            return self.set_context_error(self.request, _msg, context)

        _stages = Stage.objects.filter(rally=_rally.id)
        _stagesData = list()
        for _stage in Stage.objects.filter(rally=_rally.id):
            _stageData = dict()
            _stageData['stage_instance'] = _stage
            _stageData['sections'] = _stage.get_roadbook
            _stageData['number_of_sections'] = len(_stageData['sections'])
            _stageData['has_assistance'] = _stage.has_assistance

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

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _form = EditRallyStagesForm(self.request.POST, request=self.request, rally=_rally)
        if not _form.is_valid():
            _msg = mark_safe('Form is not valid: %s' % _form.errors)
            return self.redirect_error(self.request, _msg)

        _form.execute()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally stages edited successfully')


class AddStageView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally/edit/stage.html'

    def __init__(self, *args, **kwargs):
        super(AddStageView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(AddStageView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, self.kwargs['pk'])

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['rally'] = _rally
        context['stage_num'] = self.request.GET.get('stage_num')

        self.log.endView()
        return context


class RemoveStageView(LoginRequiredMixin, MainView):

    def __init__(self, *args, **kwargs):
        super(RemoveStageView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _stageNum = self.request.POST['stage_num']

        _stages = Stage.objects.filter(rally=_rally)\
                               .order_by('position_in_roadbook')
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
            _msg = 'Stage %s not found for rally %s' % (_stageNum, _rallyId)
            return self.redirect_error(self.request, _msg)

        self.log.endView()
        _msg = 'Rally stage %s removed successfully from rally %s' % (_stageNum, _rallyId)
        return self.redirect_success(self.request, _msg)


class AddSectionView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally/edit/stage_section.html'

    def __init__(self, *args, **kwargs):
        super(AddSectionView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = kwargs.get('pk')
        context = super(AddSectionView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, _rallyId)

        # check permissions
        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['stage_num'] = kwargs.get('stage_num')
        context['section_num'] = self.request.GET.get('section_num')

        self.log.endView()
        return context
