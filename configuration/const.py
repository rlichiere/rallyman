# -*- coding: utf-8 -*-

DEFAULT_BACKUP_FOLDER = '..\\_BKP'


class BACKUP_CONTENT(object):
    ALL = 'all'
    CONFIG = 'config'
    LOCALES = 'locales'

    @classmethod
    def getChoices(cls):
        return [cls.ALL, cls.CONFIG, cls.LOCALES]

    @classmethod
    def getDefaultChoice(cls):
        return cls.ALL

    @classmethod
    def getNeutralChoice(cls):
        return cls.ALL
