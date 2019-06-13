# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta

from threading import Thread
import time

import utils_date
import config
from .game_logic import GameLogic
from .const.lobby.rallies import RallyStatus
from .const.rally import StepStatus, GAMESTEP_MAX_LIFETIME
from .const.crons import REFRESH_RALLIES_STATUS_SECONDS, CHECK_EXPIRED_GAMESTEPS_DELAY
from .logger import Log
from ..models import GameStep, Participation, Rally


class RalliesStatusCron(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._delay = REFRESH_RALLIES_STATUS_SECONDS

    def run(self):
        _l = Log(self)
        _l.info('Cron Ready.')

        while True:
            self.process()
            time.sleep(self._delay)

    def process(self):
        _l = Log(self)
        _dtStart = dt.now()

        _allRallies = Rally.objects.all()
        for _rally in _allRallies.filter(status=RallyStatus.SCHEDULED,
                                         opened_at__lt=dt.now()):
            _l.info('Cron OPEN Scheduled rally : #%s %s' % (_rally.id, _rally.label))
            _rally.status = RallyStatus.OPENED
            _rally.save()

        for _rally in _allRallies.filter(status=RallyStatus.OPENED,
                                         started_at__lt=dt.now()):
            _l.info('Cron START Opened rally : #%s %s' % (_rally.id, _rally.label))
            _rally.status = RallyStatus.STARTED
            _rally.save()

            # close rally if it has no participations
            _participations = Participation.objects.filter(rally=_rally)
            if _participations.count() == 0:
                _rally.status = RallyStatus.FINISHED
                _rally.finished_at = utils_date.now()
                _rally.save()

                # TODO : recreate rally if it's a 'looping' one

                continue

            # initialize Rally
            GameLogic(_rally).initializeRally()
            _step = GameStep(rally=_rally, player=Participation.objects.get(rally=_rally, turn_position=1).player)
            _step.save()

        _dtEnd = dt.now()
        _l.info('Rallies status processed in %s' % (_dtEnd - _dtStart))


class ExpiredGameSteps(Thread):

    def __init__(self):
        Thread.__init__(self)
        self._delay = CHECK_EXPIRED_GAMESTEPS_DELAY

    def run(self):
        _l = Log(self)
        _l.info('Cron Ready.')

        while True:
            self.process()
            time.sleep(self._delay)

    def process(self):
        _l = Log(self)
        _dtStart = dt.now()

        _gameSteps = GameStep.objects.filter(status=StepStatus.RUNNING, rally__status=RallyStatus.STARTED)
        for _gameStep in _gameSteps:

            _part = Participation.objects.get(rally=_gameStep.rally, player=_gameStep.player)
            if _part.isLastStageFinished:
                GameLogic(_gameStep.rally).closeGameStep(_gameStep)
                continue

            _startedAt = _gameStep.started_at
            _startedAt.replace(tzinfo=utils_date.utc)
            _now = utils_date.now()
            _gameStepLifeTime = config.get('game/gamestep/max_lifetime', GAMESTEP_MAX_LIFETIME)
            _expiresAt = _startedAt + timedelta(seconds=_gameStepLifeTime)
            if _expiresAt < _now:
                GameLogic(_gameStep.rally).forcePlayerToPlay(_gameStep)
                GameLogic(_gameStep.rally).closeGameStep(_gameStep)
                _l.info('Cron CLOSE Expired gamestep: #%s %s' % (_gameStep.id, _gameStep.rally.label))

        _dtEnd = dt.now()
        _l.info('Expired gamesteps processed in %s' % (_dtEnd - _dtStart))
