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


EMPTY_CHOICE = ('', '---')


class RallyStatus(object):
    SCHEDULED = 'SCHEDULED'
    OPENED = 'OPENED'
    STARTED = 'STARTED'
    FINISHED = 'FINISHED'

    @classmethod
    def as_list(cls):
        return [cls.SCHEDULED, cls.OPENED, cls.STARTED, cls.FINISHED]

    @classmethod
    def as_choices(cls):
        return [(_s, str(_s).lower().capitalize()) for _s in cls.as_list()]

    @classmethod
    def as_choices_with_undefined(cls):
        _list = cls.as_choices()
        _list.insert(0, EMPTY_CHOICE)
        return _list

    @classmethod
    def get_default(cls):
        return cls.OPENED


LOBBY_RALLIES_PARTICIP_CHOICES = [
    EMPTY_CHOICE,
    ('True', 'Yes'),
    ('False', 'No')
]
LOBBY_RALLIES_PARTICIP_DEFAULT_KEY = LOBBY_RALLIES_PARTICIP_CHOICES[0][0]
LOBBY_RALLIES_STATUS_DEFAULT_KEY = EMPTY_CHOICE[0]
LOBBY_RALLIES_CREATOR_CHOICES = [
    EMPTY_CHOICE,
    ('me', 'Me'),
    ('notme', 'Not me')
]
LOBBY_RALLIES_CREATOR_DEFAULT_KEY = LOBBY_RALLIES_CREATOR_CHOICES[0][0]

LOBBY_RALLIES_ORDER_BY = [
    'label',
    # ('number_of_participants', 'number_of_participants'),
    # ('number_of_es', 'number_of_es'),
    'status',
    'creator',
]
LOBBY_RALLIES_ORDER_BY_DEFAULT_KEY = LOBBY_RALLIES_ORDER_BY[0]
LOBBY_RALLIES_ORDER_WAY = ['asc', 'desc']
LOBBY_RALLIES_ORDER_WAY_DEFAULT_KEY = LOBBY_RALLIES_ORDER_WAY[0]
