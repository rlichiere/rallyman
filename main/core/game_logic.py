# -*- coding:utf-8 -*-
from . import utils_date
from .logger import Log
from .const.rally import StepStatus
from .const.lobby.rallies import RallyStatus
from ..models import GameStep, Participation, Rally, Stage


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
        _l = Log(self)
        # _lp = '%s.initializeRally:' % self.__class__.__name__
        _l.info('Initialize rally [#%s %s]' % (self._rally.id, self._rally.label))

        # Create first GameStep
        _step = GameStep(rally=self._rally, player=Participation.objects.get(rally=self._rally, turn_position=1).player)
        _step.save()

        # Position cars on stage
        for _part in Participation.objects.filter(rally=self._rally):
            _part.initializeCarPosition()
            _part.initializeTimes()
        _l.debug('Initialize rally [#%s %s] done' % (self._rally.id, self._rally.label))

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
        _l = Log(self)
        _l.info('Close rally [#%s %s]' % (self._rally.id, self._rally.label))
        self._rally.status = RallyStatus.FINISHED
        self._rally.finished_at = utils_date.now()
        self._rally.save()
        _l.debug('Close rally [#%s %s] done' % (self._rally.id, self._rally.label))

    def forcePlayerToPlay(self, game_step):
        _l = Log(self)
        _l.info('Force player [%s]' % game_step.player)

        # manage a force play
        self.decrementPlayerGear(game_step)
        self.movePlayerCarForward(game_step)

        _l.debug('Force player [%s] done' % game_step.player)

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
        _l = Log(self)
        _l.info('Move player [%s]' % game_step.player)
        _participation = Participation.objects.get(rally=self._rally, player=game_step.player)
        _carPos = _participation.carPosition

        # check if player is not on last cell of section
        if not (int(_carPos['cell']) == 17):
            _participation.setCarPosition(cell=_carPos['cell'] + 1)
            _l.info('move player [%s] of one cell on section' % game_step.player)
            return

        _stageNum = _carPos['stage']
        _sectionNum = _carPos['section']
        _stage = Stage.objects.get(rally=game_step.rally, position_in_roadbook=_stageNum)
        _roadbook = _stage.get_roadbook

        _playerIsOnLastSection = False
        try:
            _nextSection = _roadbook[_sectionNum]
        except IndexError:
            _playerIsOnLastSection = True

        if not _playerIsOnLastSection:
            # player is a end of a section. move to the next section
            _participation.setCarPosition(section=_sectionNum + 1, cell=1)
            _msgFollowing = 'move player to first cell of next section'
            _l.info('Player [%s] is not on last section. %s' % (game_step.player, _msgFollowing))
            return
        _l.debug('Player [%s] is on last section' % (game_step.player))

        # player is on last section
        _playerIsOnLastStage = False
        try:
            _nextStage = Stage.objects.get(rally=game_step.rally, position_in_roadbook=_stageNum + 1)
        except Stage.DoesNotExist:
            _playerIsOnLastStage = True

        if not _playerIsOnLastStage:
            # player is at end of stage, move to the beginning of next stage
            _participation.setCarPosition(stage=_stageNum + 1, section=1, cell=0)
            _msgFollowing = 'move player to first cell of first section of next stage'
            _l.info('Player [%s] is not on last stage. %s' % (game_step.player, _msgFollowing))
            return

        # player is on last section of last stage, so the rally is finished for him
        _msgFollowing = 'so his rally is finished'
        _l.info('Player [%s] is on last section of last stage. %s' % (game_step.player, _msgFollowing))
        _participation.setLastStageFinished()
