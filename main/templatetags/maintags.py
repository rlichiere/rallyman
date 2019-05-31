# -*- coding: utf-8 -*-
from django import template

from ..core import constants

register = template.Library()


@register.simple_tag
def const(constant_name):
    """
        Returns the value of given constant.
    :param constant_name: Name of the constant to retrieve
    :type constant_name: str
    :return: value of the constant
    :rtype: str
    """
    if hasattr(constants, constant_name):
        return getattr(constants, constant_name)

    return None


class GetConstantsNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        context['constants'] = constants
        return ''


@register.tag
def get_constants(parser, params):
    return GetConstantsNode()
