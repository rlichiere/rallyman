# -*- coding: utf-8 -*-

""" Rally constants """


""" Creation """

DELAY_OPEN_TO_NEXT = 5
DELAY_START_TO_NEXT = 15

PERSISTENCE_OPEN_IN_NEXT = 5
PERSISTENCE_START_IN_NEXT = 20


""" Configuration """

MAX_PARTICIPANTS_PER_RALLY = 4
GAMESTEP_MAX_LIFETIME = 300    # Maximum lifetime of a game step, in seconds.


class StepStatus(object):
    RUNNING = 'RUNNING'
    CLOSED = 'CLOSED'

    @classmethod
    def as_list(cls):
        return [cls.RUNNING, cls.CLOSED]

    @classmethod
    def as_choices(cls):
        return [(_s, str(_s).lower().capitalize()) for _s in cls.as_list()]

    @classmethod
    def get_default(cls):
        return cls.RUNNING
