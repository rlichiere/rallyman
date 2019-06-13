# -*- coding: utf-8 -*-
from abc import abstractmethod
from datetime import timedelta

from threading import Thread
import time

import utils_date
import config
from .game_logic import GameLogic
from .const.lobby.rallies import RallyStatus
from .const.rally import StepStatus, GAMESTEP_MAX_LIFETIME
from .const import crons as const_cron
from .logger import Log
from ..models import GameStep, Participation, Rally


class MainCron(Thread):
    name = 'Implementation should use a unique name'

    def __init__(self):
        Thread.__init__(self)
        self._confPath = self._getConfPath()
        self.isActive = self._isActive()

        _delayPath = '%s/delay' % self._confPath
        _delayConstName = ('%s_DELAY' % self.name).upper()
        try:
            _delayConst = getattr(const_cron, _delayConstName)
        except AttributeError as e:
            _l = Log(self)
            _msg = 'Constant not found : const.crons.%s' % _delayConstName
            _l.error(_msg)
            raise Exception(_msg)  # todo : should raise a custom ConfigurationError
        self._delay = config.get(_delayPath, _delayConst)

    def run(self):
        _l = Log(self)
        if not self.isActive:
            _l.info('Cron not active. Skipped')
            return
        _l.info('Cron is active. Ready')

        while True:
            self.process()
            time.sleep(self._delay)

    def process(self):
        _l = Log(self)
        _dtStart = utils_date.now()
        _l.info('Cron process at %s' % _dtStart)

        try:
            self.job(_l)
        except Exception as e:
            _l.error('Unexpected %s while processing Cron %s' % (repr(e), self.name))

        _dtEnd = utils_date.now()
        _l.info('Cron done in %s' % (_dtEnd - _dtStart))

    """ Abstract """

    @abstractmethod
    def job(self, logger):
        pass

    """ Private """

    def _getConfPath(self):
        return 'cron/%s' % self.name

    def _isActive(self):
        _confPath = 'cron/%s' % self.name
        return config.get(_confPath)


class RalliesStatusCron(MainCron):
    name = 'check_rallies_status'

    def __init__(self):
        super(RalliesStatusCron, self).__init__()

    def job(self, logger):

        _allRallies = Rally.objects.all()
        for _rally in _allRallies.filter(status=RallyStatus.SCHEDULED,
                                         opened_at__lt=utils_date.now()):
            logger.info('Cron OPEN Scheduled rally : #%s %s' % (_rally.id, _rally.label))
            _rally.status = RallyStatus.OPENED
            _rally.save()

        for _rally in _allRallies.filter(status=RallyStatus.OPENED,
                                         started_at__lt=utils_date.now()):
            logger.info('Cron START Opened rally : #%s %s' % (_rally.id, _rally.label))
            _rally.status = RallyStatus.STARTED
            _rally.save()

            # close rally if it has no participations
            _participations = Participation.objects.filter(rally=_rally)
            if _participations.count() == 0:
                GameLogic(_rally).closeRally()

                continue

            # initialize Rally
            GameLogic(_rally).initializeRally()


class ExpiredGameSteps(MainCron):
    name = 'check_expired_gamesteps'

    def __init__(self):
        super(ExpiredGameSteps, self).__init__()

    def job(self, logger):

        _expiredGameSteps = 0
        _gameSteps = GameStep.objects.filter(status=StepStatus.RUNNING, rally__status=RallyStatus.STARTED)
        for _gameStep in _gameSteps:
            _gameStepLog = '#%s %s' % (_gameStep.id, _gameStep.rally.label)

            _part = Participation.objects.get(rally=_gameStep.rally, player=_gameStep.player)
            if _part.isLastStageFinished:
                logger.info('Expire gamestep: %s, Force arrived player [%s]' % (_gameStepLog, _gameStep.player))
                GameLogic(_gameStep.rally).closeGameStep(_gameStep)
                _expiredGameSteps += 1
                continue

            _startedAt = _gameStep.started_at
            _startedAt.replace(tzinfo=utils_date.utc)
            _now = utils_date.now()
            _gameStepLifeTime = config.get('game/gamestep/max_lifetime', GAMESTEP_MAX_LIFETIME)
            _expiresAt = _startedAt + timedelta(seconds=_gameStepLifeTime)
            if _expiresAt < _now:
                logger.info('Expire gamestep: %s, Force running player [%s}' % (_gameStepLog, _gameStep.player))
                GameLogic(_gameStep.rally).forcePlayerToPlay(_gameStep)
                GameLogic(_gameStep.rally).closeGameStep(_gameStep)
                _expiredGameSteps += 1
