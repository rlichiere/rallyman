# -*- coding: utf-8 -*-
from datetime import datetime as dt

from django import forms

from ..core import utils_str
from ..models import CarSkin, Participation, Stage


class CreateRallyForm(forms.Form):
    label = forms.CharField(max_length=200)
    set_opened_at = forms.BooleanField(required=False)
    opened_at = forms.DateTimeField()

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(CreateRallyForm, self).__init__(*args, **kwargs)

        self.fields['label'].initial = utils_str.get_random_phrase()
        self.fields['opened_at'].initial = dt.now()


class EditRallyStagesForm(object):

    def __init__(self, *args, **kwargs):
        self.stages = list()

        _post = args[0]
        self.rally = kwargs.pop('rally')

        _stagesCount = int(_post.get('stages_count'))
        for _stageIndex in range(1, _stagesCount + 1):
            _stageId = 'Stage_%s' % _stageIndex
            _stage = dict()

            # todo : add has_assistance if its input is set
            # _stage['has_assistance'] = True

            _stageSectionsCount = int(_post.get('%s_sections_count' % _stageId))
            _stage['sections_count'] = _stageSectionsCount

            _stage['sections'] = list()

            for _sectionIndex in range(1, _stageSectionsCount + 1):
                _sectionId = '%s_%s' % (_stageId.lower(), _sectionIndex)
                _sectionData = dict()
                # todo : try, except Missing mandatory parameter
                _sectionData['zone'] = _post['%s_zone' % _sectionId]
                _sectionData['anchor'] = _post['%s_anchor' % _sectionId]
                _sectionData['surface'] = _post['%s_surface' % _sectionId]

                _stage['sections'].append(_sectionData)

            self.stages.append(_stage)

    def is_valid(self):
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

            # todo : add has_assistance if its input is set
            # _stage['has_assistance'] = True

            for _sectionField in _stageField['sections']:

                # todo : try, except Missing mandatory parameter
                _sectionZone = _sectionField['zone']
                _sectionAnchor = _sectionField['anchor']
                _sectionSurface = _sectionField['surface']

                _stage.addSectionToRoadbook(zone=_sectionZone, surface=_sectionSurface, anchor=_sectionAnchor)
            _stage.save()

    @property
    def errors(self):
        return ''


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
