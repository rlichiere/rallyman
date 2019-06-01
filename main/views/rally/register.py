# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView

from ...core.const.rally import MAX_PARTICIPANTS_PER_RALLY
from ...generic.views import ViewHelper
from ...forms.rally import RegisterToRallyForm
from ...models import CarSkin, Participation, Rally


class RegisterToRallyView(ViewHelper, TemplateView):
    template_name = 'main/rally_register.html'

    def __init__(self, *args, **kwargs):
        super(RegisterToRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(RegisterToRallyView, self).get_context_data(**kwargs)
        _rallyId = self.kwargs['pk']
        context['form_register'] = RegisterToRallyForm(request=self.request, rally_id=_rallyId)

        _rally = Rally.objects.get(id=_rallyId)
        _participations = Participation.objects.filter(rally=_rally)
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)
        context['rally'] = _rally
        context['participations'] = _participations

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _rallyId = self.kwargs['pk']
        self.log.startView(_executor)

        _target = self.request.GET.get('target', 'main-home')
        self.log.debug(_target=_target)

        _form = RegisterToRallyForm(self.request.POST, request=self.request, rally_id=self.kwargs['pk'])
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid : %s' % _form.errors), _target)

        _rally = Rally.objects.get(id=_rallyId)
        _carSkin = CarSkin.objects.get(id=_form.cleaned_data.get('car_skin'))
        _participation = Participation(rally=_rally,
                                       player=_executor,
                                       car_skin=_carSkin,
                                       car_position=Participation.objects.filter(rally=_rallyId).count() + 1)
        _participation.save()

        self.log.endView()
        return self.redirect_success(self.request, 'Participation registered successfully', _target)
