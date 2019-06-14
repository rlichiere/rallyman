# -*- coding: utf-8 -*-
from django import template

from ..core import config
from ..core.const.lobby.rallies import RallyStatus
from ..core.logger import Log
from ..models import Rally

from . import utils


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


class GetConfigNode(template.Node):

    def __init__(self, property_name):
        self._propName = property_name

    def render(self, context):
        _log = Log(self)

        # check that given object_name is a config property
        if not hasattr(config, self._propName):
            _err = 'Unknown property in config : %s' % self._propName
            _log.error(_err)
            raise Exception(_err)

        # detect and skip reloading case in order to improve performances (and log a warning)
        if self._propName in context:
            _err = 'property %s already loaded in context' % self._propName
            _log.warning(_err)
            if config.settings.DEBUG and config.get('debug/fail_on_warning'):
                raise Exception(_err)
            return ''

        context[self._propName] = _config_mappings[self._propName]
        return ''


@register.tag
def load_config(parser, token):
    _params = token.split_contents()

    if len(_params) != 2:
        _err = '%r tag requires the name of a property to load from config' % _params[0]
        raise template.TemplateSyntaxError(_err)

    _propName = _params[1]
    return GetConfigNode(_propName)


class GetLoadDataNode(template.Node):

    def __init__(self, user, data_set):
        self._user = user
        self._dataSet = data_set
        self._mappings = {
            'participated_rallies': user_participated_rallies,
            'managed_rallies': user_managed_rallies,
        }

    def render(self, context):
        _log = Log(self)

        _user = self._user.resolve(context)
        if _user.is_anonymous:
            return ''

        # check that given dataset is expected
        if self._dataSet not in self._mappings.keys():
            raise Exception('Unknown dataset for user : %s' % self._dataSet)

        # detect and skip reloading case in order to improve performances (and log a warning)
        if self._dataSet in context:
            _err = 'dataset %s already loaded for user' % self._dataSet
            _log.warning(_err)
            if config.settings.DEBUG and config.get('debug/fail_on_warning'):
                raise Exception(_err)
            return ''

        # build data with mapped method
        context[self._dataSet] = self._mappings[self._dataSet](_user)
        return ''


@register.tag
def load_user_data(parser, token):
    _params = token.split_contents()

    if len(_params) != 3:
        _err = '%r tag requires a user and a dataset to load' % _params[0]
        raise template.TemplateSyntaxError(_err)

    _user = parser.compile_filter(_params[1])

    _dataSet = _params[2]
    return GetLoadDataNode(_user, _dataSet)


def user_participated_rallies(user):
    _data = dict()
    _status = [RallyStatus.OPENED, RallyStatus.STARTED]
    _userRallies = Rally.objects.filter(participation__player=user, status__in=_status)

    for _rally in _userRallies:
        if _rally.status not in _data:
            _data[_rally.status] = list()

        if _rally.creator == user:
            _rally.user_is_creator = True

        _data[_rally.status].append(_rally)
    return _data


def user_managed_rallies(user):
    _data = dict()
    _userManagedRallies = Rally.objects.filter(creator=user)
    for _rally in _userManagedRallies:
        if _rally.status not in _data:
            _data[_rally.status] = list()

        if _rally.creator == user:
            _rally.user_is_creator = True

            _data[_rally.status].append(_rally)
    return _data


@register.filter
def instance_model(instance):
    """
    Template filter that returns instance model name (in lower case).
    E.g. if field is Rally then {{ instance|instance_type }} will
    return 'rally'.
    """
    return type(instance).__name__.lower()


@register.filter
def instance_module(instance):
    """
    Template filter that returns instance model name (in lower case).
    E.g. if field is Rally then {{ instance|instance_type }} will
    return 'rally'.
    """
    _module = type(instance).__module__
    return _module[:_module.find('.')]


@register.tag(name='get_conf')
def get_configuration_or_constant(parser, token):
    """
    Returns the configured value at given `path` if found, otherwise returns the value of the given constant

    Takes path as first argument and constant as second argument.
    Path should be in the form of `'some/path/to/some/config/key'` or `"some/path/to/a/config/key"` ,
    Constant should be in the form [const.]module.of.the.constant.SOME_CONSTANT.

    Examples:

        * Standard case:

            ```
            {% get_conf 'some/path/key' const.some.module.SOME_CONSTANT %}
            ```

        * Shorten case:

            As `const.` prefix is not mandatory for the `constantName parameter`, it may be omitted.

            ```
            {% get_conf 'path' some_child_of_const_module.some.module.SOME_CONSTANT %}
            ```

    :param parser: the standard Parser given by the call of the tag while the template rendering
                    This object is used in the tag to compile an string into an evaluable expression,
                        which must be passed to the rendering Node in order to be evaluated (`.resolve`).
    :type parser: django.template.base.Parser
    :param token: the standard Token given by the call of the tag while the template rendering.
                    This object must be split in order to unpack tag parameters
    :type token: django.template.base.Token
    :return: found configuration-otherwise-constant value for given `path` and `constantName`
    :rtype: int, str, list, dict
    """
    _l = Log()
    bits = token.split_contents()
    error_msg = '%r tag requires a "path/to/some/config/key" followed by its corresponding constant' % bits[0]
    try:
        path = bits[1]
        constantName = bits[2]
    except ValueError:
        _l.error(error_msg)
        raise template.TemplateSyntaxError(error_msg)

    _validator = utils.validators.GetConfigurationOrConstantValidator(path, constantName)
    if not _validator.is_valid():
        _msg = 'Validation error : %s' % _validator.errors
        _l.error(_msg)
        raise Exception(_msg)

    path = _validator.cleaned_data['path']
    constantName = _validator.cleaned_data['constantName']
    _l.debug(path=path, constantName=constantName)

    constantExpression = parser.compile_filter(constantName)
    return GetConfNode(path, constantName, constantExpression)


class GetConfNode(template.Node):
    def __init__(self, path, constant_name, constant_expression):
        self.path = path
        self.constantName = constant_name
        self.constantExpression = constant_expression

    def render(self, context):
        _l = Log(self)

        _configuredValue = config.get(self.path)
        if _configuredValue:
            _l.info('use configuration for path %s : %s' % (self.path, _configuredValue))
            return _configuredValue

        _constantValue = self.constantExpression.resolve(context)
        _l.info('use constant %s for path %s : %s' % (self.constantName, self.path, _constantValue))
        return _constantValue
