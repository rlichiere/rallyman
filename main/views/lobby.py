# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from ..forms.lobby import FilterRalliesForm
from ..generic.views import ViewHelper
from ..models import Game, RallyStatus, Participation, Stage


class LobbyView(TemplateView, ViewHelper):
    template_name = 'main/lobby.html'

    def get_context_data(self, **kwargs):
        _lp = '%s.get_context_data:' % self.__class__.__name__
        _executor = self.request.user
        context = super(LobbyView, self).get_context_data(**kwargs)

        _allRallies = Game.objects.all()

        # prepare filters
        _filterForm = FilterRalliesForm(request=self.request)
        _orderBy = _filterForm.fields['order_by'].initial
        _orderWay = _filterForm.fields['order_way'].initial
        _userParticipation = _filterForm.fields['user_participation'].initial
        _rallyStatus = _filterForm.fields['rally_status'].initial
        _rallyCreator = _filterForm.fields['rally_creator'].initial
        _ralliesFilter = dict()
        _ralliesExclude = dict()

        # manage creator filter
        if _rallyCreator == 'me':
            _ralliesFilter['creator'] = _executor
        elif _rallyCreator == 'notme':
            _ralliesExclude['creator'] = _executor

        # manage rally_status filter
        if _rallyStatus not in ['-', '']:
            _ralliesFilter['status'] = _rallyStatus

        # apply filters
        _rallies = _allRallies.exclude(**_ralliesExclude)
        _rallies = _rallies.filter(**_ralliesFilter)

        _ralliesParticipations = Participation.objects.filter(game__in=_rallies)
        _ralliesParticipationsIds = _ralliesParticipations.values_list('id', flat=True)
        if _userParticipation == 'True':
            _rallies = _rallies.filter(id__in=_ralliesParticipationsIds)
        elif _userParticipation == 'False':
            _rallies = _rallies.exclude(id__in=_ralliesParticipationsIds)

        # order by database fields
        if _orderBy and _orderBy in ['label', 'status', 'creator']:
            _rallies = _rallies.order_by('%s%s' % ('-' if _orderWay == 'desc' else '', _orderBy))

        # browse elected games, and add temporary attributes
        _allStages = Stage.objects.all()
        for _rally in _rallies:
            _rallyParticipations = _ralliesParticipations.filter(game=_rally)
            setattr(_rally, 'participants', _rallyParticipations)
            setattr(_rally, 'participants_count', _rallyParticipations.count())

            _checkIfJoignable = True
            _checkIfQuitable = True
            try:
                if _rally.status in [RallyStatus.SCHEDULED, RallyStatus.STARTED]:
                    _checkIfJoignable = False

                if _rally.status == RallyStatus.FINISHED:
                    _checkIfJoignable = False
                    _checkIfQuitable = False

                _ = _rallyParticipations.get(player=_executor)

                if _checkIfQuitable:
                    setattr(_rally, 'is_quitable', True)

            except Participation.DoesNotExist:
                if _checkIfJoignable:
                    setattr(_rally, 'is_joignable', True)

            _stages = _allStages.filter(game=_rally)
            setattr(_rally, 'stages', _stages)
            setattr(_rally, 'stages_count', _stages.count())

        # order by
        if _orderBy and _orderBy in ['number_of_participants', 'number_of_es']:
            # todo : manage ordering by logic data
            pass

        context['order_by'] = _orderBy
        context['order_way'] = _orderWay
        context['form_filter'] = _filterForm
        context['user_rallies'] = _rallies
        return context
