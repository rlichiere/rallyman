# -*- coding: utf-8 -*-


class Zones(object):
    C = 'C'
    J = 'J'
    L = 'L'
    V = 'V'

    @classmethod
    def as_list(cls):
        return [cls.C, cls.J, cls.L, cls.V]

    @classmethod
    def as_choices(cls):
        return [(_s, _s) for _s in cls.as_list()]

    @classmethod
    def get_default(cls):
        return cls.C


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


class ZoneEntries(object):
    entries = [1, 2, 3, 4, 5, 6]

    @classmethod
    def as_list(cls):
        return cls.entries

    @classmethod
    def as_choices(cls):
        return [(_s, _s) for _s in cls.as_list()]

    @classmethod
    def get_default(cls):
        return cls.entries[0]
