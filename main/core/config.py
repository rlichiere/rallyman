# -*- coding: utf-8 -*-
import sys

from rallyman import settings as _main_settings

from configuration.configurator import Configurator, Configuration
from ..core import const as _main_const
from ..core import crons as _crons
from ..core import utils_dict as _utils_dict


""" Main constants """
const = _main_const

""" Configured data """
_confData = Configuration('data', 'rallyman\\config\\config.yml')
Configurator.register(_confData)
data = Configurator.load('data')


""" Configured Locales """
# todo : this dictionary should contain localization data loaded from localized templates
_confLocales = Configuration('locales', 'rallyman\\config\\locales.yml')
Configurator.register(_confLocales)
locales = Configurator.load('locales')


""" Main settings """
settings = _main_settings


""" Exploitation """


def get(path, default=None):
    _accessed = _utils_dict.access(data, path)
    if not _accessed:
        return default
    return _accessed


def get_config(path, constant):
    """
        Returns configuration value at given `path` if found, otherwise returns given `constant`.

        Equivalent to the eponymous tag.

        Example:

            > config.get_config('path/of/some/configuration/key', const.module.of.some.constant.SOME_CONSTANT)

    :param path:
    :param constant:
    :return:
    """
    _value = get(path)
    if _value is not None:
        return _value

    return constant


class PageSizeConfiguration(object):

    pageSizes = get_config('lobby/rallies/pagination/pagesizes',
                           const.lobby.rallies.PAGINATION__PAGESIZES)

    @classmethod
    def as_choices(cls):
        return [(_, str(_)) for _ in cls.pageSizes]

    @classmethod
    def get_default(cls):
        return cls.pageSizes[0]

    @classmethod
    def get_min(cls):
        return min(cls.pageSizes)


configurations = dict()
configurations[PageSizeConfiguration.__class__.__name__] = PageSizeConfiguration


""" Crons """

crons = [
    _crons.RalliesStatusCron(),
    _crons.ExpiredGameSteps(),
]

if sys.argv[1] == 'runserver':
    for _cron in crons:
        _cron.start()
