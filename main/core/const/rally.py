# -*- coding: utf-8 -*-

""" Rally creation """

ROUND_OPENED_AT_MINUTES = 5
ROUND_STARTED_AT_MINUTES = 5
DELAY_STARTED_AT_MINUTES = 15


""" Rally configuration """

MAX_PARTICIPANTS_PER_RALLY = 4


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


GAMESTEP_MAX_LIFETIME = 300    # Maximum lifetime of a game step, in seconds.
