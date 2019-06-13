# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionDenied

from ....core.const.rally import MAX_PARTICIPANTS_PER_RALLY
from ....generic.views import MainView, MainTemplateView
from ....models import CarSkin, Participation, Rally
from ....forms.rally import InviteToRallyForm


class ParticipantsView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_edit_participants.html'

    def __init__(self, *args, **kwargs):
        super(ParticipantsView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        context = super(ParticipantsView, self).get_context_data(**kwargs)
        context['ariane'] = ['edit-rally', 'participants']
        _rally = self.get_object_or_404(Rally, _rallyId)

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _participations = Participation.objects.filter(rally=_rallyId).order_by('turn_position')
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)
        context['participations'] = _participations
        context['rally'] = _rally

        self.log.endView()
        return context


class ChangePositionView(LoginRequiredMixin, MainView):

    def __init__(self, *args, **kwargs):
        super(ChangePositionView, self).__init__(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = kwargs.get('pk')
        _participantId = self.request.POST['player_id']
        _way = self.request.POST['change_way']

        _rally = self.get_object_or_404(Rally, _rallyId)

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _participant = self.get_object_or_404(User, _participantId)

        _part = Participation.objects.get(rally=_rally, player=_participant)
        _oldPosition = _part.turn_position

        if _way == 'up':
            _newPosition = int(_part.turn_position - 1)
        elif _way == 'down':
            _newPosition = int(_part.turn_position + 1)
        else:
            raise Exception('Unexpected change_way : %s' % _way)
        _otherParticipant = Participation.objects.get(rally=_rally, turn_position=_newPosition)

        # update position of the participant
        _part.turn_position = _newPosition
        _part.save()

        # update position of the other participant
        _otherParticipant.turn_position = _oldPosition
        _otherParticipant.save()

        self.log.endView()
        return self.return_success(self.request, 'Changed participant position in rally')


class InviteParticipantView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_invite_participant.html'

    def __init__(self, *args, **kwargs):
        super(InviteParticipantView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        context = super(InviteParticipantView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, _rallyId)

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

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

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _invitedPlayerId = request.POST['invited_player']
        _carSkinId = request.POST['car_skin']
        _invitedPlayer = self.get_object_or_404(User, _invitedPlayerId)
        _carSkin = self.get_object_or_404(CarSkin, _carSkinId)

        _part = Participation(rally=_rally, player=_invitedPlayer, car_skin=_carSkin)
        _part.save()

        self.log.endView()
        return self.redirect_success(self.request, 'Participant invited successfully')


class KickParticipantView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_kick_participant.html'

    def __init__(self, *args, **kwargs):
        super(KickParticipantView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        _rallyId = self.kwargs['pk']
        _kickedUserId = self.kwargs['uid']
        context = super(KickParticipantView, self).get_context_data(**kwargs)
        _rally = self.get_object_or_404(Rally, _rallyId)

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        context['rally'] = _rally
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

        if (_executor.id is not _rally.creator.id) and not _executor.is_superuser:
            raise PermissionDenied

        _kickedParticipant = self.get_object_or_404(User, _kickedUserId)

        _part = Participation.objects.get(rally=_rally, player=_kickedParticipant)
        _part.delete()

        self.log.endView()
        return self.redirect_success(self.request, 'Participant kicked from rally')
