# -*- coding: utf-8 -*-
import json

from django.db import models

from ..core.const import zone as const_zone
from .rally import Rally


class Stage(models.Model):
    rally = models.ForeignKey(help_text='Rally targeted by this membership.',
                              to=Rally,
                              null=True, blank=True,
                              on_delete=models.CASCADE)
    position_in_roadbook = models.IntegerField(help_text='Position of the stage in the roadbook',
                                               default=1)
    roadbook = models.CharField(help_text='Roadbook of the stage.'
                                          ' JSON list of the board anchors that defines each stage.',
                                max_length=1024,
                                default='[]')
    has_assistance = models.BooleanField(help_text='Tells if an assistance is available at the end of stage.',
                                         default=False)

    @property
    def roadbook_as_label(self):
        _res = ' - '.join(
            ['%s%s%s' % (_zone['zone'], _zone['anchor'], '*' if _zone['surface'] == const_zone.ZoneSurfaces.SNOW else '')
             for _zone in self.get_roadbook]
        )
        if self.has_assistance:
            _res += ' - [R]'
        return _res

    @property
    def get_roadbook(self):
        return json.loads(self.roadbook)

    def clearRoadbook(self):
        self.roadbook = '[]'
        self.save()

    def addSectionToRoadbook(self, zone, surface, anchor, save=False):
        _roadbook = self.get_roadbook
        _roadbook.append({
            'zone': zone,
            'surface': surface,
            'anchor': anchor,
        })
        self.roadbook = json.dumps(_roadbook)

        if save:
            self.save()
