# -*- coding: utf-8 -*-


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
