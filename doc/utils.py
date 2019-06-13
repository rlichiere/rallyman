# -*- coding: utf-8 -*-


_DOC_PAGES = [
    {'key': 'home',      'title': 'Home',              'path': 'md',   'file': 'HOME.md'},
    {'key': 'sign',      'title': 'User registration', 'path': 'md',   'file': 'SIGN.md'},
    {'key': 'lobby',     'title': 'Lobby',             'path': 'md',   'file': 'LOBBY.md'},
    {'key': 'rally',     'title': 'Rally',             'path': 'md',   'file': 'RALLY.md'},
    {'key': 'changelog', 'title': 'Changelog',         'path': 'md',   'file': 'CHANGELOG.md', 'requires': 'superuser'},
    {'key': 'readme',    'title': 'Read me',           'path': '..\\', 'file': 'README.md',    'requires': 'superuser'},
    {'key': 'todo',      'title': 'Todo',              'path': '..\\', 'file': 'TODO.md',      'requires': 'superuser'},
]


class DocPages(object):

    @classmethod
    def getDefaultPageConfiguration(cls):
        return _DOC_PAGES[0]

    @classmethod
    def getPageConfiguration(cls, page_key):
        _index = 0
        for _conf in _DOC_PAGES:
            _index += 1
            if _conf['key'] == page_key:
                cls._addContextData(_conf, _index)
                return _conf

        _conf = cls.getDefaultPageConfiguration()
        cls._addContextData(_conf, index=1)
        return _conf

    @classmethod
    def getPagesConfiguration(cls, executor):
        _confs = list()
        _index = 0
        for _conf in _DOC_PAGES:
            _index += 1
            _requires = _conf.get('requires')
            if (_requires == 'superuser') and not executor.is_superuser:
                continue

            cls._addContextData(_conf, _index)
            _confs.append(_conf)

        return _confs

    @classmethod
    def _addContextData(cls, conf, index):
        conf['index'] = index
        _path = '' if conf['path'] == '' else ('%s\\' % conf['path'])
        conf['filepath'] = '%s%s' % (_path, conf['file'])
