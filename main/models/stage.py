# -*- coding: utf-8 -*-
import json

from django.db import models

from ..core import constants
from .game import Game


class Stage(models.Model):
    game = models.ForeignKey(help_text='Game targeted by this membership.',
                             to=Game,
                             on_delete=models.CASCADE)
    position_in_roadbook = models.IntegerField(help_text='Position of the stage in the roadbook',
                                               default=1,
                                               unique=True)
    roadbook = models.CharField(help_text='Roadbook of the stage.'
                                          ' JSON list of the board anchors that defines each stage.',
                                max_length=1024,
                                default='[]')
    has_assistance = models.BooleanField(help_text='Tells if an assistance is available at the end of stage.',
                                         default=False)

    @property
    def roadbook_as_label(self):
        _res = ' - '.join(
            ['%s%s%s' % (_zone['zone'], _zone['anchor'], '*' if _zone['surface'] == constants.ZoneSurfaces.SNOW else '')
             for _zone in self.get_roadbook]
        )
        if self.has_assistance:
            _res += ' - [R]'
        return _res

    @property
    def get_roadbook(self):
        return json.loads(self.roadbook)
