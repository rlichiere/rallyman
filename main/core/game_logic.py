# -*- coding:utf-8 -*-
from ..core import utils_date
from ..core.const.rally import StepStatus, MAX_PARTICIPANTS_PER_RALLY
from ..core.const.lobby.rallies import RallyStatus
from ..models import GameStep, Participation, Rally


class GameData(object):

    def __init__(self, rally):
        self._rally = rally
        self._data = dict()

    def load(self, rally_id):
        pass


class GameLogic(object):

    def __init__(self, rally=None, rally_id=None):
        self._rally = rally if rally else Rally.objects.get(id=rally_id)

    def initializeRally(self):

        # Create first GameStep
        _step = GameStep(rally=self._rally, player=Participation.objects.get(rally=self._rally, turn_position=1).player)
        _step.save()

        # Position cars on stage
        for _part in Participation.objects.filter(rally=self._rally):
            _part.initializeCarPosition()
            _part.initializeTimes()

    def getNextPlayer(self, player):
        _participations = Participation.objects.filter(rally=self._rally)
        _nextTurn = Participation.objects.get(player=player).turn_position + 1
        if _nextTurn > _participations.count():
            _nextTurn = 1
        return _participations.get(turn_position=_nextTurn).player

    def closeGameStep(self, game_step=None, game_step_id=None):

        # Close current gamestep
        _gameStep = game_step if game_step else GameStep.objects.get(id=game_step_id)
        _gameStep.status = StepStatus.CLOSED
        _gameStep.save()

        # Check if rally is finished
        if self.isRallyFinished:
            self.closeRally()
            return

        self.prepareNextStep(_gameStep)

    def prepareNextStep(self, game_step):
        _nextPlayer = self.getNextPlayer(game_step.player)
        _newStep = GameStep(rally=self._rally, player=_nextPlayer, index=game_step.index + 1)
        _newStep.save()

    @property
    def isRallyFinished(self):
        for _part in Participation.objects.filter(rally=self._rally):
            if not _part.isLastStageFinished:
                return False
        return True

    def closeRally(self):
        self._rally.status = RallyStatus.FINISHED
        self._rally.finished_at = utils_date.now()
        self._rally.save()

    def forcePlayerToPlay(self, game_step):

        # manage a force play
        self.decrementPlayerGear(game_step)
        self.movePlayerCarForward(game_step)

    def decrementPlayerGear(self, game_step):
        _participation = Participation.objects.get(rally=self._rally, player=game_step.player)
        _dashboard = _participation.dashboard
        _gear = _dashboard['gear']
        if _gear > 1:
            _gear = _gear - 1
        else:
            _gear = 1
        _dashboard['gear'] = _gear
        _participation.setDashboard(_dashboard)

    def movePlayerCarForward(self, game_step):

        _participation = Participation.objects.get(rally=self._rally, player=game_step.player)
        _carPosition = _participation.carPosition

        # TODO : move car to next cell
        # if not on last cell of section:
        #       _carPosition['cell'] = _carPosition['cell'] + 1
        # else:
        #       if roadbook has next section:
        #           put car on first cell of next section
        #       else:
        #           rally is finished for player
        if not (int(_carPosition['cell']) == 42):
            _carPosition['cell'] = _carPosition['cell'] + 1
            _participation.setCarPosition(_carPosition)

        else:
            if False:
                # todo : player is at end of stage, should go at beginning of next stage
                pass
            else:
                _participation.setLastStageFinished()
