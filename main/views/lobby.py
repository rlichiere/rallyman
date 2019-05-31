# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from ..forms.lobby import FilterGamesForm
from ..generic.views import ViewHelper
from ..models import Game, GameStatus, Participation, Stage


class LobbyView(TemplateView, ViewHelper):
    template_name = 'main/lobby.html'

    def get_context_data(self, **kwargs):
        _lp = '%s.get_context_data:' % self.__class__.__name__
        _executor = self.request.user
        context = super(LobbyView, self).get_context_data(**kwargs)

        _allGames = Game.objects.all()

        # prepare filters
        _filterForm = FilterGamesForm(request=self.request)
        _orderBy = _filterForm.fields['order_by'].initial
        _orderWay = _filterForm.fields['order_way'].initial
        _userParticipation = _filterForm.fields['user_participation'].initial
        _gameStatus = _filterForm.fields['game_status'].initial
        _gameCreator = _filterForm.fields['game_creator'].initial
        _gamesFilter = dict()
        _gamesExclude = dict()

        # manage creator filter
        if _gameCreator == 'me':
            _gamesFilter['creator'] = _executor
        elif _gameCreator == 'notme':
            _gamesExclude['creator'] = _executor

        # manage game_status filter
        if _gameStatus not in ['-', '']:
            _gamesFilter['status'] = _gameStatus

        # apply filters
        _games = _allGames.exclude(**_gamesExclude)
        _games = _games.filter(**_gamesFilter)

        _gamesParticipations = Participation.objects.filter(game__in=_games)
        _gamesParticipationsIds = _gamesParticipations.values_list('id', flat=True)
        if _userParticipation == 'True':
            _games = _games.filter(id__in=_gamesParticipationsIds)
        elif _userParticipation == 'False':
            _games = _games.exclude(id__in=_gamesParticipationsIds)

        # order by database fields
        if _orderBy and _orderBy in ['label', 'status', 'creator']:
            _games = _games.order_by('%s%s' % ('-' if _orderWay == 'desc' else '', _orderBy))

        # browse elected games, and add temporary attributes
        _allStages = Stage.objects.all()
        for _game in _games:
            _gameParticipations = _gamesParticipations.filter(game=_game)
            setattr(_game, 'participants', _gameParticipations)
            setattr(_game, 'participants_count', _gameParticipations.count())

            _checkIfJoignable = True
            _checkIfQuitable = True
            try:
                if _game.status in [GameStatus.SCHEDULED, GameStatus.STARTED]:
                    _checkIfJoignable = False

                if _game.status == GameStatus.FINISHED:
                    _checkIfJoignable = False
                    _checkIfQuitable = False

                _ = _gameParticipations.get(player=_executor)

                if _checkIfQuitable:
                    setattr(_game, 'is_quitable', True)

            except Participation.DoesNotExist:
                if _checkIfJoignable:
                    setattr(_game, 'is_joignable', True)

            _stages = _allStages.filter(game=_game)
            setattr(_game, 'stages', _stages)
            setattr(_game, 'stages_count', _stages.count())

        # order by
        if _orderBy and _orderBy in ['number_of_participants', 'number_of_es']:
            # todo : manage ordering by logic data
            pass

        context['order_by'] = _orderBy
        context['order_way'] = _orderWay
        context['form_filter'] = _filterForm
        context['user_games'] = _games
        return context
