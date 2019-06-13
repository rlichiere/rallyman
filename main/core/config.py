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


""" Crons """

crons = [
    _crons.RalliesStatusCron(),
    _crons.ExpiredGameSteps(),
]

if sys.argv[1] == 'runserver':
    for _cron in crons:
        _cron.start()
