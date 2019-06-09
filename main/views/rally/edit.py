# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.safestring import mark_safe

from ...core.const.lobby.rallies import RallyStatus
from ...core.const.rally import MAX_PARTICIPANTS_PER_RALLY
from ...generic.views import MainTemplateView, MainView
from ...models import CarSkin, Participation, Rally, Stage
from ...forms.rally import EditRallyStagesForm, InviteToRallyForm


class EditRallyView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_edit_roadbook.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})
        context = super(EditRallyView, self).get_context_data(**kwargs)

        # check permissions

        context['ariane'] = ['edit_rally', 'roadbook']
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

        _form = EditRallyStagesForm(self.request.POST, request=self.request, rally=_rally)
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid: %s' % _form.errors))

        _form.execute()

        self.log.endView()
        return self.redirect_success(self.request, 'Rally stages edited successfully')


class EditRallyAddStageView(LoginRequiredMixin, MainTemplateView):
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


class EditRallyRemoveStageView(LoginRequiredMixin, MainView):

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


class EditRallyAddZoneView(LoginRequiredMixin, MainTemplateView):
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


class EditRallyParticipantsView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_edit_participants.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyParticipantsView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        context = super(EditRallyParticipantsView, self).get_context_data(**kwargs)
        context['ariane'] = ['edit-rally', 'participants']
        _rally = self.get_object_or_404(Rally, _rallyId)
        context['rally'] = _rally

        context['participations'] = Participation.objects.filter(rally=_rallyId)
        _participations = Participation.objects.filter(rally=_rallyId)
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)
        context['participations'] = _participations

        self.log.endView()
        return context


class EditRallyInviteParticipantView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_invite_participant.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyInviteParticipantView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        context = super(EditRallyInviteParticipantView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, _rallyId)

        context['form_invite'] = InviteToRallyForm(request=self.request, rally_id=_rallyId)

        context['available_players'] = User.objects.all().exclude(id=1)\
                                                         .exclude(participation__rally=_rallyId)\
                                                         .order_by('first_name', 'last_name')

        _participations = Participation.objects.filter(rally=_rally)
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)

        self.log.debug(availableSlotsCount=_availableSlotsCount)

        context['car_skins'] = CarSkin.objects.all()
        context['rally'] = _rally

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rallyId = kwargs.get('pk')
        _rally = self.get_object_or_404(Rally, _rallyId)
        _invitedPlayerId = request.POST['invited_player']
        _carSkinId = request.POST['car_skin']
        _invitedPlayer = self.get_object_or_404(User, _invitedPlayerId)
        _carSkin = self.get_object_or_404(CarSkin, _carSkinId)

        _part = Participation(rally=_rally, player=_invitedPlayer, car_skin=_carSkin)
        _part.save()

        self.log.endView()
        return self.redirect_success(self.request, 'Participant invited successfully')


class EditRallyKickParticipantView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_kick_participant.html'

    def __init__(self, *args, **kwargs):
        super(EditRallyKickParticipantView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        _kickedUserId = self.kwargs['uid']
        context = super(EditRallyKickParticipantView, self).get_context_data(**kwargs)

        context['rally'] = self.get_object_or_404(Rally, _rallyId)
        context['kicked_player'] = self.get_object_or_404(User, _kickedUserId)

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor,
                           redirect_to=self.request.GET.get('redirect'),
                           redirect_to_kwargs={'pk': self.request.GET.get('redirect_pk')})

        _rallyId = kwargs.get('pk')
        _kickedUserId = self.kwargs['uid']

        _rally = self.get_object_or_404(Rally, _rallyId)
        _kickedParticipant = self.get_object_or_404(User, _kickedUserId)

        _part = Participation.objects.get(rally=_rally, player=_kickedParticipant)
        _part.delete()

        self.log.endView()
        return self.redirect_success(self.request, 'Participant kicked from rally')
