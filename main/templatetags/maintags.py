# -*- coding: utf-8 -*-
from django import template

from ..core import const

register = template.Library()


class GetConstantsNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['const'] = const
        return ''


@register.tag
def get_constants(parser, params):
    return GetConstantsNode()
