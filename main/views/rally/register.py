# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.safestring import mark_safe

from ...core.const.rally import MAX_PARTICIPANTS_PER_RALLY
from ...generic.views import MainTemplateView
from ...forms.rally import RegisterToRallyForm
from ...models import CarSkin, Participation, Rally


class RegisterToRallyView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_register.html'

    def __init__(self, *args, **kwargs):
        super(RegisterToRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(RegisterToRallyView, self).get_context_data(**kwargs)
        _rallyId = self.kwargs['pk']
        context['form_register'] = RegisterToRallyForm(request=self.request, rally_id=_rallyId)

        try:
            _rally = Rally.objects.get(id=_rallyId)
            context['rally'] = _rally
        except Rally.DoesNotExist:
            self.log.error('Unknown Rally %s' % _rallyId)
            raise Http404
        except Exception as e:
            _msg = 'Unexpected error while retrieving Rally #%s : %s' % (_rallyId, repr(e))
            return self.set_context_error(self.request, _msg, context)

        _participations = Participation.objects.filter(rally=_rally)
        _availableSlotsCount = MAX_PARTICIPANTS_PER_RALLY - _participations.count()
        setattr(_rally, 'available_slots_count', _availableSlotsCount)
        context['participations'] = _participations

        context['car_skins'] = CarSkin.objects.all()

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _rallyId = self.kwargs['pk']
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        _form = RegisterToRallyForm(self.request.POST, request=self.request, rally_id=_rallyId)
        if not _form.is_valid():
            return self.redirect_error(self.request, mark_safe('Form is not valid: %s' % _form.errors))

        try:
            _rally = Rally.objects.get(id=_rallyId)
        except Rally.DoesNotExist:
            return self.redirect_error(self.request, 'Unknown Rally %s' % _rallyId)
        except Exception as e:
            _msg = 'Unexpected error while retrieving Rally #%s : %s' % (_rallyId, repr(e))
            return self.redirect_error(self.request, _msg)

        _carSkin = CarSkin.objects.get(id=_form.cleaned_data.get('car_skin'))
        _position = Participation.objects.filter(rally=_rallyId).count() + 1
        _participation = Participation(rally=_rally,
                                       player=_executor,
                                       car_skin=_carSkin,
                                       car_position=_position,
                                       turn_position=_position)
        _participation.save()

        self.log.endView()
        return self.redirect_success(self.request, 'Participation registered successfully')


class UnRegisterFromRallyView(LoginRequiredMixin, MainTemplateView):
    template_name = 'main/rally_unregister.html'

    def __init__(self, *args, **kwargs):
        super(UnRegisterFromRallyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(UnRegisterFromRallyView, self).get_context_data(**kwargs)

        _rallyId = self.kwargs['pk']

        try:
            _rally = Rally.objects.get(id=_rallyId)
            context['rally'] = _rally
        except Rally.DoesNotExist:
            self.log.error('Unknown Rally %s' % _rallyId)
            raise Http404
        except Exception as e:
            _msg = 'Unexpected error while retrieving Rally #%s : %s' % (_rallyId, repr(e))
            return self.set_context_error(self.request, _msg, context)

        self.log.endView()
        return context

    def post(self, request, *args, **kwargs):
        _executor = self.request.user
        _rallyId = self.kwargs['pk']
        _redirect = self.request.GET.get('redirect', 'main-home')
        self.log.startView(_executor, _redirect)

        _logDesc = 'for user %s to rally %s' % (_executor, _rallyId)
        try:
            _participation = Participation.objects.get(rally__id=_rallyId, player=_executor)
        except Participation.DoesNotExist:
            return self.redirect_error(self.request, 'Unknown participation %s' % _logDesc)
        except Exception as e:
            _msg = 'Unexpected error while retrieving Participation %s : %s' % (_logDesc, repr(e))
            return self.redirect_error(self.request, _msg)

        _removedPosition = _participation.turn_position
        _participation.delete()

        # update position of other participants
        _participations = Participation.objects.filter(rally__id=_rallyId)
        for _participation in _participations:
            if _participation.turn_position > _removedPosition:
                _newPosition = int(_participation.turn_position) - 1
                _participation.turn_position = _newPosition
                _participation.car_position = _newPosition
                _participation.save()
                self.log.debug('Updated position for player %s : %s' % (_participation.player.get_full_name(),
                                                                        _participation.car_position))
        self.log.endView()
        return self.redirect_success(self.request, 'Participation registered successfully')
