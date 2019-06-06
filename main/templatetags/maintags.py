# -*- coding: utf-8 -*-
from django import template

from ..core import config
from ..core.const.lobby.rallies import RallyStatus
from ..core.logger import Log
from ..models import Rally


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
