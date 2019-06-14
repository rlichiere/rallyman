# -*- coding: utf-8 -*-
from ...const.form import EMPTY_CHOICE


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


PARTICIP_CHOICES = [
    EMPTY_CHOICE,
    ('1', 'Yes'),
    ('0', 'No')
]
PARTICIP_DEFAULT_KEY = PARTICIP_CHOICES[0][0]
STATUS_DEFAULT_KEY = EMPTY_CHOICE[0]
CREATOR_CHOICES = [
    EMPTY_CHOICE,
    ('me', 'Me'),
    ('nm', 'Not me')
]
CREATOR_DEFAULT_KEY = CREATOR_CHOICES[0][0]

PAGINATION__PAGESIZES = [
    10,
    25,
    50,
    100,
]

ORDER_BY = [
    'label',
    # ('number_of_participants', 'number_of_participants'),
    # ('number_of_es', 'number_of_es'),
    'status',
    'creator',
]
ORDER_BY_DEFAULT_KEY = ORDER_BY[0]
ORDER_WAY = ['a', 'd']
ORDER_WAY_DEFAULT_KEY = ORDER_WAY[0]

RALLY_LABEL_MAX_LENGTH_IN_LIST = 60
RALLY_LABEL_MAX_LENGTH_IN_LIST_SLICE = ':%s' % RALLY_LABEL_MAX_LENGTH_IN_LIST
