# -*- coding: utf-8 -*-
from datetime import datetime as dt
from django import forms

# from tempus_dominus.widgets import DateTimePicker

from ..core import utils_str


class CreateRallyForm(forms.Form):
    label = forms.CharField(max_length=200)
    set_opened_at = forms.BooleanField(required=False)
    opened_at = forms.DateTimeField(label='Registration opening date', help_text='Registration opening date help', )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CreateRallyForm, self).__init__(*args, **kwargs)

        self.fields['label'].initial = utils_str.get_random_phrase()
        self.fields['opened_at'].initial = dt.now()
