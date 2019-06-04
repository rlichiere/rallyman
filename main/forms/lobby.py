# -*- coding: utf-8 -*-
from django import forms

from ..core.const.lobby import rallies as const_rallies


class FilterRalliesForm(forms.Form):
    usr_part = forms.ChoiceField(choices=const_rallies.PARTICIP_CHOICES,
                                 required=False)
    rly_stat = forms.ChoiceField(choices=const_rallies.RallyStatus.as_choices_with_undefined(),
                                 required=False)
    rly_crea = forms.ChoiceField(choices=const_rallies.CREATOR_CHOICES,
                                 required=False)
    ord_b = forms.CharField(initial=const_rallies.ORDER_BY_DEFAULT_KEY,
                            required=False)
    ord_w = forms.CharField(initial=const_rallies.ORDER_WAY_DEFAULT_KEY,
                            required=False)

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        super(FilterRalliesForm, self).__init__(*args, **kwargs)

        self.fields['usr_part'].initial = request.GET.get('usr_part',
                                                          const_rallies.PARTICIP_DEFAULT_KEY)
        self.fields['rly_stat'].initial = request.GET.get('rly_stat',
                                                          const_rallies.STATUS_DEFAULT_KEY)
        self.fields['rly_crea'].initial = request.GET.get('rly_crea',
                                                          const_rallies.CREATOR_DEFAULT_KEY)
        self.fields['ord_b'].initial = request.GET.get('ord_b',
                                                       const_rallies.ORDER_BY_DEFAULT_KEY)
        self.fields['ord_w'].initial = request.GET.get('ord_w',
                                                       const_rallies.ORDER_WAY_DEFAULT_KEY)


class PaginationPageSizeForm(forms.Form):
    CHOICES = (
        (10, '10'),
        (25, '25'),
        (50, '50'),
        (100, '100'),
    )
    available_page_sizes = forms.ChoiceField(label='Show x item', choices=CHOICES, required=False)
    selected_page_size = forms.CharField(label='Show x item', required=False)
