# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


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
