# -*- coding: utf-8 -*-
from datetime import datetime as dt
from datetime import timedelta

from django import forms
from django.core.validators import RegexValidator

from ..core import utils_date, utils_str
from ..core.const import rally as const_rally
from ..models import CarSkin, Participation, Stage


class CreateRallyForm(forms.Form):
    label = forms.CharField(max_length=200,
                            validators=[
                                RegexValidator(regex='^[a-zA-Z0-9 _-]*$',
                                               message='Accepted characters: a..z A..Z 0..9 _ - <space>')
                            ], label='Label', help_text='Help for Label')
    set_opened_at = forms.BooleanField(required=False)
    opened_at = forms.DateTimeField()
    started_at = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CreateRallyForm, self).__init__(*args, **kwargs)

        self.fields['label'].initial = utils_str.get_random_phrase()
        _now = dt.now()
        self.fields['opened_at'].initial = utils_date.round_to_next_minutes(_now,
                                                                            const_rally.ROUND_OPENED_AT_MINUTES)

        _rounded = utils_date.round_to_next_minutes(_now, const_rally.ROUND_STARTED_AT_MINUTES)
        self.fields['started_at'].initial = _rounded + timedelta(minutes=const_rally.DELAY_STARTED_AT_MINUTES)

    def clean_started_at(self):
        _startedAt = self.cleaned_data['started_at']
        _openedAt = self.cleaned_data['opened_at']

        if _openedAt > _startedAt:
            raise forms.ValidationError('Start date must be later than Open date')

        return self.cleaned_data['started_at']


class EditRallyStagesForm(object):

    def __init__(self, *args, **kwargs):
        _lp = '%s.__init__:' % self.__class__.__name__
        self.stages = list()
        self._errors = dict()

        _post = args[0]
        self.rally = kwargs.pop('rally')

        _stagesCount = int(_post.get('stages_count'))
        for _stageIndex in range(1, _stagesCount + 1):
            _stageId = 'Stage_%s' % _stageIndex
            _stage = dict()

            # todo : add has_assistance if its input is set
            _pnHasAssistance = '%s_has_assistance' % _stageId
            _stage['has_assistance'] = bool(_pnHasAssistance in _post.keys())

            _stageSectionsCount = int(_post['%s_sections_count' % _stageId])
            _stage['sections_count'] = _stageSectionsCount

            _stage['sections'] = list()

            for _sectionIndex in range(1, _stageSectionsCount + 1):
                _sectionId = '%s_%s' % (_stageId.lower(), _sectionIndex)
                _sectionData = dict()

                _pZone = '%s_zone' % _sectionId
                _pAnchor = '%s_anchor' % _sectionId
                _pSurface = '%s_surface' % _sectionId
                try:
                    _sectionData['zone'] = _post[_pZone]
                except KeyError:
                    self._errors[_pZone] = 'Missing parameter : zone'
                    return
                try:
                    _sectionData['anchor'] = _post[_pAnchor]
                except KeyError:
                    self._errors[_pAnchor] = 'Missing parameter : anchor'
                    return
                try:
                    _sectionData['surface'] = _post[_pSurface]
                except KeyError:
                    self._errors[_pSurface] = 'Missing parameter : surface'
                    return

                _stage['sections'].append(_sectionData)

            self.stages.append(_stage)

    def is_valid(self):
        if len(self._errors) > 0:
            return False
        return True

    def execute(self):
        _stageIndex = 0
        for _stageField in self.stages:
            _stageIndex += 1

            try:
                _stage = Stage.objects.get(rally=self.rally, position_in_roadbook=_stageIndex)
                _stage.clearRoadbook()
            except Stage.DoesNotExist:
                _stage = Stage(rally=self.rally, position_in_roadbook=_stageIndex)
                _stage.save()

            # set has_assistance
            _stage.has_assistance = bool(_stageField['has_assistance'])

            for _sectionField in _stageField['sections']:
                _sectionZone = _sectionField['zone']
                _sectionAnchor = _sectionField['anchor']
                _sectionSurface = _sectionField['surface']

                _stage.addSectionToRoadbook(zone=_sectionZone, surface=_sectionSurface, anchor=_sectionAnchor)
            _stage.save()

    @property
    def errors(self):
        return self._errors


class RegisterToRallyForm(forms.Form):
    car_skin = forms.ChoiceField(choices=CarSkin.as_choices(CarSkin.availableSkins()))

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        _rallyId = kwargs.pop('rally_id')
        super(RegisterToRallyForm, self).__init__(*args, **kwargs)

        # initialize car_skins field with remaining skins for the given rally
        _usedSkinsIds = Participation.objects.filter(rally=_rallyId).values_list('car_skin', flat=True)
        _skinsChoices = self.fields['car_skin'].choices
        _remainingChoices = list()
        for _skinChoice in _skinsChoices:
            if _skinChoice[0] not in _usedSkinsIds:
                _remainingChoices.append(_skinChoice)

        self.fields['car_skin'].choices = _remainingChoices
