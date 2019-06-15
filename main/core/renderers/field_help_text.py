# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe


class FormFieldHelpTextRenderer(object):

    def __init__(self, help_text):
        """

        :param help_text: help_text of a FormField
        :type help_text: dict
        """
        self._helpText = help_text

    def render(self):
        _html = '<p>%s</p>' % self._helpText['intro']
        _html += '<p>Constraints:'
        _html += '<ul class=\'fa-ul\'>'
        for _validation in self._helpText['constraints']:
            _html += '<li><span class=\'fa-li\'><i class=\'fas fa-caret-right\'></i></span>%s</li>' % _validation
        _html += '</ul></p>'

        return mark_safe(_html)
