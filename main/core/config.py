# -*- coding: utf-8 -*-
from rallyman import settings as _main_settings

from ..core import const as _main_const
from ..core import utils_dict as _utils_dict


""" Main constants """
const = _main_const


""" Configured data """
# todo : this dictionary should contain configuration data loaded from an external (non-git) file
data = {
    'config_key_1': 'config_key_1_value',
    'config_key_2': 'config_key_2_value',

    'debug': {
        'fail_on_warning': False,
    }
}


""" Configured Locales """
# todo : this dictionary should contain localization data loaded from localized templates
locales = {
    'KEY_1': 'KEY_1_VALUE',
    'KEY_2': 'KEY_2_VALUE',
}


""" Main settings """
settings = _main_settings


""" Exploitation """


def get(path, default=None):
    return _utils_dict.access(data, path, default)
