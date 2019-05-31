# -*- coding: utf-8 -*-
from django import forms

from ..core import constants


ORDER_BY_CHOICES = [
    ('label', 'label'),
    # ('number_of_participants', 'number_of_participants'),
    # ('number_of_es', 'number_of_es'),
    ('status', 'status'),
    ('creator', 'creator'),
]

ORDER_WAY_CHOICES = [
    ('asc', 'asc'),
    ('desc', 'desc'),
]


class FilterGamesForm(forms.Form):
    user_participation = forms.ChoiceField(choices=[('', '---'), ('True', 'Yes'), ('False', 'No')], required=False)
    game_status = forms.ChoiceField(choices=constants.GameStatus.as_choices_with_undefined(), required=False)
    game_creator = forms.ChoiceField(choices=[('', '---'), ('me', 'Me'), ('notme', 'Not me')], required=False)
    order_by = forms.CharField(required=False, initial=ORDER_BY_CHOICES[0][0])
    order_way = forms.CharField(required=False, initial=ORDER_WAY_CHOICES[0][0])

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(FilterGamesForm, self).__init__(*args, **kwargs)

        self.fields['user_participation'].initial = request.GET.get('user_participation', '')
        self.fields['game_status'].initial = request.GET.get('game_status', '')
        self.fields['game_creator'].initial = request.GET.get('game_creator', '')
        self.fields['order_by'].initial = request.GET.get('order_by', ORDER_BY_CHOICES[0][0])
        self.fields['order_way'].initial = request.GET.get('order_way', ORDER_WAY_CHOICES[0][0])
