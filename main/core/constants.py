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


class ZoneSurfaces(object):
    DRY = 'DRY'
    SNOW = 'SNOW'

    @classmethod
    def as_list(cls):
        return [cls.DRY, cls.SNOW]

    @classmethod
    def as_choices(cls):
        return [(_s, _s) for _s in cls.as_list()]

    @classmethod
    def get_default(cls):
        return cls.DRY


class GameStatus(object):
    SCHEDULED = 'SCHEDULED'
    OPENED = 'OPENED'
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'

    @classmethod
    def as_list(cls):
        return [cls.SCHEDULED, cls.OPENED, cls.STARTED, cls.FINISHED]

    @classmethod
    def as_choices(cls):
        return [(_s, _s) for _s in cls.as_list()]

    @classmethod
    def as_choices_with_undefined(cls):
        _list = cls.as_choices()
        _list.insert(0, ('', '---'))
        return _list

    @classmethod
    def get_default(cls):
        return cls.OPENED
