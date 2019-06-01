# -*- coding: utf-8 -*-


import logging
logger = logging.getLogger('main_logger')


class Log(object):

    def __init__(self, caller=None):
        self._caller = caller
        self._executor = None
        self._redirect_to = None

    """ Public """

    def debug(self, msg=None, *arg_msg, **kw_msg):
        logger.debug(self._expandParams(level='DEBUG', msg=msg, *arg_msg, **kw_msg))

    def info(self, msg=None, *arg_msg, **kw_msg):
        logger.info(self._expandParams(level='INFO', msg=msg, *arg_msg, **kw_msg))

    def infoIndirect(self, msg=None, *arg_msg, **kw_msg):
        rv = logger.findCaller()
        logger.info(self._expandParams(level='INFO', msg=msg, rv=rv, *arg_msg, **kw_msg))

    def warning(self, msg=None, *arg_msg, **kw_msg):
        logger.warning(self._expandParams(level='WARNING', msg=msg, *arg_msg, **kw_msg))

    def error(self, msg=None, *arg_msg, **kw_msg):
        logger.error(self._expandParams(level='ERROR', msg=msg, *arg_msg, **kw_msg))

    def exception(self, msg=None, *arg_msg, **kw_msg):
        logger.exception(self._expandParams(level='EXCEPTION', msg=msg, *arg_msg, **kw_msg))

    """ View conveniency methods """

    def setExecutor(self, executor):
        self._executor = executor

    def getRedirect(self):
        return self._redirect_to

    def setRedirect(self, redirect_to):
        self._redirect_to = redirect_to

    def startView(self, executor=None, redirect_to=None):
        if executor is not None:
            self.setExecutor(executor)

        if redirect_to is not None:
            self.setRedirect(redirect_to)

        self.infoIndirect('Start')

    def endView(self):
        self.infoIndirect('End.')

    """ Private """

    def _expandParams(self, level, msg, rv=None, *arg_msg, **kw_msg):
        _msg = self._expandMessage(msg, *arg_msg, **kw_msg)

        if rv is None:
            rv = logger.findCaller()
        lr = logger.makeRecord(name='main_logger', level=level, msg=_msg,
                               fn=rv[0], lno=rv[1], func=rv[2],
                               args=[], exc_info=None)
        _caller = ('%s.' % self._caller.__class__.__name__) if self._caller != '' else ''
        _executor = ('[%s] ' % self._executor) if self._executor is not None else ''
        return '%s %s%s%s:%3d: %s' % (lr.module, _executor, _caller, lr.funcName, lr.lineno, _msg)

    @classmethod
    def _expandMessage(cls, msg='', *arg_msg, **kw_msg):
        _joignables = list()

        if msg not in [None, '']:
            _joignables.append(msg)

        if len(arg_msg) > 0:
            _argMsg = ', '.join(_arg for _arg in arg_msg)
            _joignables.append(_argMsg)

        if len(kw_msg) > 0:
            _kwMsg = ', '.join('%s : %s' % (_k, _v) for _k, _v in kw_msg.iteritems())
            _joignables.append(_kwMsg)

        return ', '.join(_joignables)
