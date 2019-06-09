# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from ....core.const.rally import MAX_PARTICIPANTS_PER_RALLY
from ....generic.views import MainTemplateView
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
        context['rally'] = _rally

        context['participations'] = Participation.objects.filter(rally=_rallyId)
        _participations = Participation.objects.filter(rally=_rallyId)
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)
        context['participations'] = _participations

        self.log.endView()
        return context


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
