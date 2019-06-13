# -*- coding: utf-8 -*-


class Gears(object):
    NEUTRAL = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5

    @classmethod
    def default(cls):
        return cls.NEUTRAL

    @classmethod
    def as_list(cls):
        return [cls.NEUTRAL, cls.FIRST, cls.SECOND, cls.THIRD, cls.FOURTH, cls.FIFTH]


class Tyre(object):
    def __init__(self, name, max_dry_warns, max_snow_warns):
        self.name = name
        self.max_warns_on_dry = max_dry_warns
        self.max_warns_on_snow = max_snow_warns


class Tyres(object):
    DRY = Tyre('DRY', max_dry_warns=3, max_snow_warns=2)
    SNOW = Tyre('SNOW', max_dry_warns=3, max_snow_warns=3)

    @classmethod
    def default(cls):
        return cls.DRY

    @classmethod
    def as_list(cls):
        return [cls.DRY, cls.SNOW]


INITIAL = {
    'gear': Gears.default(),
    'tyre': Tyres.default().name,
}
