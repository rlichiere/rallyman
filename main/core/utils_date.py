# -*- coding: utf-8 -*-
from datetime import timedelta


def round_to_next_minutes(date, minutes):
    _nowMinutes = date.minute

    # calculate remaining minutes to next given minutes
    _moduled = _nowMinutes % minutes
    _remainingToNextMinutes = minutes - _moduled

    # build the timedelta remaining to the given date, rounded to given minutes
    _next = timedelta(minutes=_remainingToNextMinutes - 1, seconds=60 - date.second)

    return date + _next
