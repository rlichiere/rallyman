# -*- coding: utf-8 -*-


class CarDirections(object):
    UP = 0
    UP_RIGHT = 45
    RIGHT = 90
    DOWN_RIGHT = 135
    DOWN = 180
    DOWN_LEFT = 225
    LEFT = 270
    UP_LEFT = 315

    @classmethod
    def get_default(cls):
        return cls.UP

