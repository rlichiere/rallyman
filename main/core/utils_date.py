# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta, tzinfo


def round_to_next_minutes(date, minutes):
    _nowMinutes = date.minute

    # calculate remaining minutes to next given minutes
    _moduled = _nowMinutes % minutes
    _remainingToNextMinutes = minutes - _moduled

    # build the timedelta remaining to the given date, rounded to given minutes
    _next = timedelta(minutes=_remainingToNextMinutes - 1, seconds=60 - date.second)

    return date + _next


ZERO = timedelta(0)


class UTC(tzinfo):

    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


def now():
    return dt.now(utc)
