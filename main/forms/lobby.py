# -*- coding: utf-8 -*-
from django import forms

from ..core import constants


class FilterRalliesForm(forms.Form):
    usr_part = forms.ChoiceField(choices=constants.LOBBY_RALLIES_PARTICIP_CHOICES,
                                 required=False)
    rly_stat = forms.ChoiceField(choices=constants.RallyStatus.as_choices_with_undefined(),
                                 required=False)
    rly_crea = forms.ChoiceField(choices=constants.LOBBY_RALLIES_CREATOR_CHOICES,
                                 required=False)
    ord_b = forms.CharField(initial=constants.LOBBY_RALLIES_ORDER_BY_DEFAULT_KEY,
                            required=False)
    ord_w = forms.CharField(initial=constants.LOBBY_RALLIES_ORDER_WAY_DEFAULT_KEY,
                            required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(FilterRalliesForm, self).__init__(*args, **kwargs)

        self.fields['usr_part'].initial = request.GET.get('usr_part',
                                                          constants.LOBBY_RALLIES_PARTICIP_DEFAULT_KEY)
        self.fields['rly_stat'].initial = request.GET.get('rly_stat',
                                                          constants.LOBBY_RALLIES_STATUS_DEFAULT_KEY)
        self.fields['rly_crea'].initial = request.GET.get('rly_crea',
                                                          constants.LOBBY_RALLIES_CREATOR_DEFAULT_KEY)
        self.fields['ord_b'].initial = request.GET.get('ord_b',
                                                       constants.LOBBY_RALLIES_ORDER_BY_DEFAULT_KEY)
        self.fields['ord_w'].initial = request.GET.get('ord_w',
                                                       constants.LOBBY_RALLIES_ORDER_WAY_DEFAULT_KEY)
