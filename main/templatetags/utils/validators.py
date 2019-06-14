# -*- coding: utf-8 -*-
import re


class GetConfigurationOrConstantValidator(object):

    path_regexp = re.compile(r"""['"]?(?P<path>[a-zA-Z0-9_./]+)['"]?""", re.VERBOSE | re.UNICODE)
    constantName_regexp = re.compile(r"""(?P<const_name>[\w_.]+)""", re.VERBOSE | re.UNICODE)

    def __init__(self, path, constant_name):
        self.path = path
        self.constantName = constant_name

        self.cleaned_data = dict()
        self.errors = False

    def is_valid(self):

        # check validity of `path`
        match = self.path_regexp.match(self.path)
        if not match:
            self._setError('path', 'Parse error')
            return False
        _matchedData = match.groupdict()
        if _matchedData['path'] != self.path[1:-1]:
            self._setError('path', 'Format error on parameter path : %s - %s' % (self.path[1:-1], _matchedData['path']))
            return False

        _parts = self.path[1:-1].split('/')
        for _part in _parts:
            # check that each part is not empty (i.e. avoids double dots)
            if _part == '':
                self._setError('path', 'Empty folder found for path : %s' % self.path)
                return False

        if self.path[0] not in ["'", '"']:
            self._setError('path', 'First character of path should be a quote or double-quote')
            return False

        if self.path[-1] != self.path[0]:
            self._setError('path', 'Last character of path should be a quote or double-quote')
            return False

        self.cleaned_data['path'] = self.path[1:-1]

        # check validity of `constantName`
        match = self.constantName_regexp.match(self.constantName)
        if not match:
            self._setError('constantName', 'Parse error')
            return False

        _parts = self.constantName.split('.')
        for _part in _parts:

            # check that each part is not empty (i.e. avoids double dots)
            if _part == '':
                self._setError('path', 'Empty module found for path : %s' % self.path)
                return False

            # - check that each part starts by an alphabetical (i.e. not an `int`, nor a `_` or `-`)
            if not _part[0].isalpha():
                self._setError('path', 'Invalid first char for module %s in constant : %s' % (_part, self.path))
                return False

            # - check that each part ends by an alphanumeric (i.e. not a `_` nor `-`)
            if not _part[-1].isalnum():
                self._setError('path', 'Invalid last char for module %s in constant : %s' % (_part, self.path))
                return False

        if not self.constantName.startswith('const.'):
            # add 'const.' prefix if missing
            self.constantName = 'const.%s' % self.constantName

        self.cleaned_data['constantName'] = self.constantName
        if self.errors:
            return False
        return True

    def _setError(self, field, message):
        if not self.errors:
            self.errors = list()
        self.errors.append({
            'field': field,
            'error': message,
        })
