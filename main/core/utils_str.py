# -*- coding: utf-8 -*-
from random import choice as rand_choice
import string

from ..core.const import dictionnaries as const_dicts


def generate_random(length=1, chars=None):
    _chars = string.ascii_letters + string.digits if chars is None else chars
    return ''.join(rand_choice(_chars) for x in range(0, length))


def get_random_phrase(separator=' '):
    _syn = rand_choice(const_dicts.RALLY_SYNONYMS).capitalize()
    _adj = rand_choice(const_dicts.ADJECTIVES)
    _noun = rand_choice(const_dicts.NOUNS)

    return '{syn}{sep}of{sep}the{sep}{adj}{sep}{noun}'.format(syn=_syn, adj=_adj, noun=_noun, sep=separator)
