# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from .skin import CarSkin
from .game import Game


class Participation(models.Model):
    game = models.ForeignKey(help_text='Game to which the user participates.',
                             to=Game)
    player = models.ForeignKey(help_text='Player which participates to a game.',
                               to=User)
    turn_position = models.IntegerField(help_text='Turn position of the player in the game.',
                                        default=1)
    car_skin = models.ForeignKey(help_text='Skin file of the car.',
                                 to=CarSkin)
    car_position = models.CharField(help_text='Position of the car in the game.',
                                    max_length=1024,
                                    default='{}')

    def __str__(self):
        return '%s - %s' % (self.game, self.player)
