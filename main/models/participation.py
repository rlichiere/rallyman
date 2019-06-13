# -*- coding: utf-8 -*-
from datetime import timedelta
import json

from django.db import models
from django.contrib.auth.models import User

from .skin import CarSkin
from .rally import Rally

from ..core.const import dashboard as const_dashboard


TIME_DATA_ZERO = {
        'hours': 0,
        'minutes': 0,
        'seconds': 0,
    }


class Participation(models.Model):
    rally = models.ForeignKey(help_text='Rally to which the user participates.',
                              null=True, blank=True,
                              to=Rally)
    player = models.ForeignKey(help_text='Player which participates to a rally.',
                               to=User)
    turn_position = models.IntegerField(help_text='Turn position of the player in the rally.',
                                        default=1)
    car_skin = models.ForeignKey(help_text='Skin file of the car.',
                                 to=CarSkin)
    car_position = models.CharField(help_text='Position of the player\'s car in the rally.',
                                    max_length=1024,
                                    default='{}')
    dashboard_data = models.CharField(help_text='Dashboard of the player\'s car in the rally.',
                                      max_length=1024,
                                      default=json.dumps(const_dashboard.INITIAL))

    times_data = models.CharField(help_text='Times of the player\'s car in the rally.',
                                  max_length=1024,
                                  default='{}')

    def __str__(self):
        return '%s - %s' % (self.rally, self.player)

    @property
    def carPosition(self):
        return json.loads(self.car_position)

    def setCarPosition(self, stage=None, section=None, cell=None):
        _carPos = self.carPosition

        if stage is not None:
            _carPos['stage'] = stage
        if section is not None:
            _carPos['section'] = section
        if cell is not None:
            _carPos['cell'] = cell

        self.car_position = json.dumps(_carPos)
        self.save()

    @property
    def dashboard(self):
        return json.loads(self.dashboard_data)

    def setDashboard(self, dashboard):
        self.dashboard_data = json.dumps(dashboard)
        self.save()

    def getStageTime(self, stage_num):
        return json.loads(self.times_data[stage_num])

    def addStageTime(self, stage_num, seconds):
        _stageTime = self.getStageTime(stage_num)
        _stageTime['hours'] += seconds / 3600
        _stageTime['minutes'] += (seconds % 3600) / 60
        _stageTime['seconds'] += (seconds % 3600) % 60
        self.times_data = json.dumps(_stageTime)
        self.save()

    def initializeCarPosition(self):
        _data = {
            'stage': 1,
            'section': 1,
            'cell': 0
        }
        self.car_position = json.dumps(_data)
        self.save()

    def initializeTimes(self):
        _data = {
            1: TIME_DATA_ZERO
        }
        self.times_data = json.dumps(_data)
        self.save()

    @property
    def isLastStageFinished(self):
        _carPosition = json.loads(self.car_position)
        if _carPosition['stage'] != 0:
            return False
        return True

    def setLastStageFinished(self):
        self.setCarPosition(stage=0, cell=0)
