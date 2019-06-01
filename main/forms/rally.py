# -*- coding: utf-8 -*-
from datetime import datetime as dt

from django import forms

from ..core import utils_str
from ..models import CarSkin, Participation


class CreateRallyForm(forms.Form):
    label = forms.CharField(max_length=200)
    set_opened_at = forms.BooleanField(required=False)
    opened_at = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CreateRallyForm, self).__init__(*args, **kwargs)

        self.fields['label'].initial = utils_str.get_random_phrase()
        self.fields['opened_at'].initial = dt.now()


class RegisterToRallyForm(forms.Form):
    car_skin = forms.ChoiceField(choices=CarSkin.as_choices(CarSkin.availableSkins()))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        _rallyId = kwargs.pop('rally_id')
        _executor = request.user
        super(RegisterToRallyForm, self).__init__(*args, **kwargs)

        # initialize car_skins field with remaining skins for the given rally
        _usedSkinsIds = Participation.objects.filter(rally=_rallyId).values_list('car_skin', flat=True)
        _skinsChoices = self.fields['car_skin'].choices
        _remainingChoices = list()
        for _skinChoice in _skinsChoices:
            if _skinChoice[0] not in _usedSkinsIds:
                _remainingChoices.append(_skinChoice)
        self.fields['car_skin'].choices = _remainingChoices
