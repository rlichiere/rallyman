# -*- coding: utf-8 -*-
from random import randint, choice as rand_choice

from ..core.const import dictionnaries as const_dicts


def get_random_phrase(separator=' '):
    _syn = rand_choice(const_dicts.RALLY_SYNONYMS).capitalize()
    _adj = rand_choice(const_dicts.ADJECTIVES)
    _noun = rand_choice(const_dicts.NOUNS)

    return '{syn}{sep}of{sep}the{sep}{adj}{sep}{noun}'.format(syn=_syn, adj=_adj, noun=_noun, sep=separator)
