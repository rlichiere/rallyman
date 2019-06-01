# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from .skin import CarSkin
from .rally import Rally


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
    car_position = models.CharField(help_text='Position of the car in the rally.',
                                    max_length=1024,
                                    default='{}')

    def __str__(self):
        return '%s - %s' % (self.rally, self.player)
