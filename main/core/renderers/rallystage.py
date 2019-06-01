# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from ...models.stage import Stage


class RallyStagesRenderer(object):

    def __init__(self, rally):
        self.rally = rally
        self.stages = Stage.objects.filter(rally=rally)

    def as_table(self):
        _res = '<table>'
        _res += '<tr><th>SS</th><th>Roadbook</th></tr>'
        _idx = 1
        for _stage in self.stages:
            _res += '<tr><td>{index}</td><td>{roadbook}</td></tr>'.format(index=_idx,
                                                                          roadbook=_stage.roadbook_as_label)
            _idx += 1

        _res += '</table>'
        return mark_safe(_res)
