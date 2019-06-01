# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from ..core.const.lobby.rallies import RallyStatus
from ..forms.lobby import FilterRalliesForm
from ..generic.views import ViewHelper
from ..models import Rally, Participation, Stage


class LobbyView(TemplateView, ViewHelper):
    template_name = 'main/lobby.html'

    def get_context_data(self, **kwargs):
        _lp = '%s.get_context_data:' % self.__class__.__name__
        _executor = self.request.user
        context = super(LobbyView, self).get_context_data(**kwargs)

        _allRallies = Rally.objects.all()

        # prepare filters
        _filterForm = FilterRalliesForm(request=self.request)
        _orderBy = _filterForm.fields['ord_b'].initial
        _orderWay = _filterForm.fields['ord_w'].initial
        _userParticipation = _filterForm.fields['usr_part'].initial
        _rallyStatus = _filterForm.fields['rly_stat'].initial
        _rallyCreator = _filterForm.fields['rly_crea'].initial
        _ralliesFilter = dict()
        _ralliesExclude = dict()

        # manage creator filter
        if _rallyCreator == 'me':
            _ralliesFilter['creator'] = _executor
        elif _rallyCreator == 'nm':
            _ralliesExclude['creator'] = _executor

        # manage rally status filter
        if _rallyStatus not in ['-', '']:
            _ralliesFilter['status'] = _rallyStatus

        # apply filters
        _rallies = _allRallies.exclude(**_ralliesExclude)
        _rallies = _rallies.filter(**_ralliesFilter)

        _ralliesParticipations = Participation.objects.filter(rally__in=_rallies)
        _ralliesParticipationsIds = _ralliesParticipations.values_list('id', flat=True)
        if not _executor.is_anonymous:
            if _userParticipation == '1':
                _rallies = _rallies.filter(id__in=_ralliesParticipationsIds)
            elif _userParticipation == '0':
                _rallies = _rallies.exclude(id__in=_ralliesParticipationsIds)

        # order by database fields
        if _orderBy and _orderBy in ['label', 'status', 'creator', 'created_at', 'opened_at']:
            _rallies = _rallies.order_by('%s%s' % ('-' if _orderWay == 'd' else '', _orderBy))

        # browse elected rally, and add temporary attributes
        _allStages = Stage.objects.all()
        for _rally in _rallies:
            _rallyParticipations = _ralliesParticipations.filter(rally=_rally)
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

                if _executor.is_anonymous:
                    raise Participation.DoesNotExist

                _ = _rallyParticipations.get(player=_executor)

                if _checkIfQuitable:
                    setattr(_rally, 'is_quitable', True)

            except Participation.DoesNotExist:
                if _checkIfJoignable:
                    setattr(_rally, 'is_joignable', True)

            _stages = _allStages.filter(rally=_rally)
            setattr(_rally, 'stages', _stages)
            setattr(_rally, 'stages_count', _stages.count())

        # order by
        if _orderBy and _orderBy in ['number_of_participants', 'number_of_es']:
            # todo : manage ordering by logic data
            pass

        context['form_filter'] = _filterForm
        context['user_rallies'] = _rallies
        return context
