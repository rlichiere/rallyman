# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class RallyParticipationsRenderer(object):

    def __init__(self, model_participation, rally):
        self.rally = rally
        self.participations = model_participation.objects.filter(rally=rally).order_by('turn_position')

    def as_table(self):
        _res = '<table>'
        _res += '<tr><th>SS</th><th>Player</th><th>Position in turn</th></tr>'
        _idx = 1
        for _participation in self.participations:
            _res += '<tr><td>{index}</td><td>{player}</td><td>{turn_position}</td></tr>'.format(
                index=_idx,
                player=_participation.player.get_full_name(),
                turn_position=_participation.turn_position)
            _idx += 1

        _res += '</table>'
        return mark_safe(_res)
