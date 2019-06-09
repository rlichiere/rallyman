# -*- coding: utf-8 -*-
from datetime import datetime as dt
from threading import Thread
import time

from ..core.const.lobby.rallies import RallyStatus
from ..core.const.crons import REFRESH_RALLIES_STATUS_SECONDS
from ..core.logger import Log
from ..models import Rally


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

        _dtEnd = dt.now()
        _l.info('Rallies status processed in %s' % (_dtEnd - _dtStart))
