# -*- coding: utf-8 -*-
from random import randint

from ..core.const import dictionnaries as const_dicts


def get_random_phrase(separator=' '):
    _syn = const_dicts.RALLY_SYNONYMS[randint(0, len(const_dicts.RALLY_SYNONYMS) - 1)].capitalize()
    _adj = const_dicts.ADJECTIVES[randint(0, len(const_dicts.ADJECTIVES) - 1)]
    _noun = const_dicts.NOUNS[randint(0, len(const_dicts.NOUNS) - 1)]
    return '{syn}{sep}of{sep}the{sep}{adj}{sep}{noun}'.format(syn=_syn, adj=_adj, noun=_noun, sep=separator)
