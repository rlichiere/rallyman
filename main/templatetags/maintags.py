# -*- coding: utf-8 -*-
from django import template

from ..core import config
from ..core.logger import Log


register = template.Library()


@register.filter
def concat(left, right):
    return '%s%s' % (str(left), str(right))


_config_mappings = {
    'const': config.const,
    'data': config.data,
    'locales': config.locales,
    'settings': config.settings,
}


class GetConstantsNode(template.Node):

    def __init__(self, object_name):
        self._objectName = object_name

    def render(self, context):
        _log = Log(self)
        # todo : should try to detect reloading in order to skip it (and log a warning)
        # problem to solve : context.keys() fails because this ContextDict is a list of dict
        if not hasattr(config, self._objectName):
            _err = 'Unknown object_name in config : %s' % self._objectName
            _log.error(_err)
            raise Exception(_err)

        if self._objectName in context:
            _err = 'object_name already loaded in context : %s' % self._objectName
            _log.warning(_err)
            if config.settings.DEBUG and config.get('debug/fail_on_warning'):
                raise Exception(_err)
            return ''

        context[self._objectName] = _config_mappings[self._objectName]
        return ''


@register.tag
def load_config(parser, token):
    _params = token.split_contents()
    _tagName = _params[0]

    if len(_params) != 2:
        _err = '%r tag requires the name of an object to load' % _tagName
        raise template.TemplateSyntaxError(_err)

    _objectName = _params[1]

    if _objectName not in _config_mappings.keys():
        _err = 'Unexpected object name %r for tag %r ' % (_objectName, _tagName)
        raise template.TemplateSyntaxError(_err)

    return GetConstantsNode(_objectName)
