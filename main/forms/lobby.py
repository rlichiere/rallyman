# -*- coding: utf-8 -*-
from django import forms

from ..core import constants


class FilterRalliesForm(forms.Form):
    user_participation = forms.ChoiceField(choices=constants.LOBBY_RALLIES_PARTICIP_CHOICES,
                                           required=False)
    rally_status = forms.ChoiceField(choices=constants.RallyStatus.as_choices_with_undefined(),
                                     required=False)
    rally_creator = forms.ChoiceField(choices=constants.LOBBY_RALLIES_CREATOR_CHOICES,
                                      required=False)
    order_by = forms.CharField(initial=constants.LOBBY_RALLIES_ORDER_BY_DEFAULT_KEY,
                               required=False)
    order_way = forms.CharField(initial=constants.LOBBY_RALLIES_ORDER_WAY_DEFAULT_KEY,
                                required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(FilterRalliesForm, self).__init__(*args, **kwargs)

        self.fields['user_participation'].initial = request.GET.get('user_participation',
                                                                    constants.LOBBY_RALLIES_PARTICIP_DEFAULT_KEY)
        self.fields['rally_status'].initial = request.GET.get('rally_status',
                                                              constants.LOBBY_RALLIES_STATUS_DEFAULT_KEY)
        self.fields['rally_creator'].initial = request.GET.get('rally_creator',
                                                               constants.LOBBY_RALLIES_CREATOR_DEFAULT_KEY)
        self.fields['order_by'].initial = request.GET.get('order_by',
                                                          constants.LOBBY_RALLIES_ORDER_BY_DEFAULT_KEY)
        self.fields['order_way'].initial = request.GET.get('order_way',
                                                           constants.LOBBY_RALLIES_ORDER_WAY_DEFAULT_KEY)
