# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from ..core.const.lobby.rallies import RallyStatus
from ..forms.lobby import FilterRalliesForm
from ..generic.views import ViewHelper
from ..models import Rally, Participation, Stage


class LobbyView(ViewHelper, TemplateView):
    template_name = 'main/lobby.html'

    def __init__(self, *args, **kwargs):
        super(LobbyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(LobbyView, self).get_context_data(**kwargs)

        _allRlys = Rally.objects.all()

        # prepare filters
        _form = FilterRalliesForm(request=self.request)
        _orderBy = _form.fields['ord_b'].initial
        _orderWay = _form.fields['ord_w'].initial
        _userPart = _form.fields['usr_part'].initial
        _rallyStatus = _form.fields['rly_stat'].initial
        _rallyCreator = _form.fields['rly_crea'].initial
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
        _rallies = _allRlys.exclude(**_ralliesExclude).filter(**_ralliesFilter)

        # manage user_participation
        _rlysParts = Participation.objects.filter(rally__in=_rallies)
        _rlysPartsIds = _rlysParts.values_list('id', flat=True)
        if not _executor.is_anonymous:
            if _userPart == '1':
                _rallies = _rallies.filter(id__in=_rlysPartsIds)
            elif _userPart == '0':
                _rallies = _rallies.exclude(id__in=_rlysPartsIds)

        # order by database fields
        if _orderBy and _orderBy in ['label', 'status', 'creator', 'created_at', 'opened_at']:
            _rallies = _rallies.order_by('%s%s' % ('-' if _orderWay == 'd' else '', _orderBy))

        # browse elected rally, and add temporary attributes
        _allStages = Stage.objects.all()
        for _rally in _rallies:
            _rlyParts = _rlysParts.filter(rally=_rally)
            setattr(_rally, 'participants', _rlyParts)
            setattr(_rally, 'participants_count', _rlyParts.count())

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

                _ = _rlyParts.get(player=_executor)

                if _checkIfQuitable:
                    setattr(_rally, 'is_quitable', True)

            except Participation.DoesNotExist:
                if _checkIfJoignable:
                    setattr(_rally, 'is_joignable', True)

            _stages = _allStages.filter(rally=_rally)
            setattr(_rally, 'stages', _stages)
            setattr(_rally, 'stages_count', _stages.count())

        # order by
        if _orderBy and _orderBy in ['number_of_participants', 'number_of_ss']:
            # todo : manage ordering by logic data
            pass

        context['form_filter'] = _form
        context['user_rallies'] = _rallies

        self.log.endView()
        return context
