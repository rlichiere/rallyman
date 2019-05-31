# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from ..models import Stage


class CarSkinRenderer(object):

    def __init__(self, car_skin):
        self.carSkin = car_skin

    def as_image(self, direction=None):

        _style = ''
        if direction is not None:
            _style += ' transform: rotate({direction}deg);'.format(direction=direction)

        if _style != '':
            _style = 'style="%s"' % _style

        return mark_safe('<img src="/static/main/car_skins/{file}" {style}/>'
                         .format(file=self.carSkin.file, style=_style))


class RoadbookRenderer(object):

    def __init__(self, roadbook_data):
        self.roadbook = roadbook_data

    def as_list(self):
        _res = '<ul>'
        for _zoneData in self.roadbook:
            _res += '<li>%s%s - %s</li>' % (_zoneData['zone'], _zoneData['anchor'], _zoneData['surface'])
        _res += '</ul>'
        return mark_safe(_res)


class GameStagesRenderer(object):

    def __init__(self, game):
        self.game = game
        self.stages = Stage.objects.filter(game=game)

    def as_table(self):
        _res = '<table>'
        _res += '<tr><th>ES</th><th>Roadbook</th></tr>'
        _idx = 1
        for _stage in self.stages:
            _res += '<tr><td>{index}</td><td>{roadbook}</td></tr>'.format(index=_idx,
                                                                          roadbook=_stage.roadbook_as_label)
            _idx += 1

        _res += '</table>'
        return mark_safe(_res)
