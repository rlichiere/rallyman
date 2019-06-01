# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class RoadbookRenderer(object):

    def __init__(self, roadbook_data):
        self.roadbook = roadbook_data

    def as_list(self):
        _res = '<ul>'
        for _zoneData in self.roadbook:
            _res += '<li>%s%s - %s</li>' % (_zoneData['zone'], _zoneData['anchor'], _zoneData['surface'])
        _res += '</ul>'
        return mark_safe(_res)
