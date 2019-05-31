# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import TemplateView, FormView

from .forms import SignUpForm, UserProfileForm, UserProfilePasswordChangeForm, FilterGamesForm
from .generic.views import ViewHelper
from .models import Game, GameStatus, Participation, Stage


class HomeView(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        return context


class LobbyView(TemplateView, ViewHelper):
    template_name = 'main/lobby.html'

    def get_context_data(self, **kwargs):
        _lp = '%s.get_context_data:' % self.__class__.__name__
        _executor = self.request.user
        context = super(LobbyView, self).get_context_data(**kwargs)

        _allGames = Game.objects.all()

        # prepare filters
        _filterForm = FilterGamesForm(request=self.request)
        _userParticipation = _filterForm.fields['user_participation'].initial

        _gameStatus = _filterForm.fields['game_status'].initial
        _gameCreator = _filterForm.fields['game_creator'].initial
        _gamesFilter = dict()
        _gamesExclude = dict()

        # manage creator filter
        if _gameCreator == 'me':
            _gamesFilter['creator'] = _executor
        elif _gameCreator == 'notme':
            _gamesExclude['creator'] = _executor

        # manage game_status filter
        if _gameStatus not in ['-', '']:
            _gamesFilter['status'] = _gameStatus

        # apply filters
        _games = _allGames.exclude(**_gamesExclude)
        _games = _games.filter(**_gamesFilter)

        _gamesParticipations = Participation.objects.filter(game__in=_games)
        _gamesParticipationsIds = _gamesParticipations.values_list('id', flat=True)
        if _userParticipation == 'True':
            _games = _games.filter(id__in=_gamesParticipationsIds)
        elif _userParticipation == 'False':
            _games = _games.exclude(id__in=_gamesParticipationsIds)

        # browse elected games, and add temporary attributes
        _allStages = Stage.objects.all()
        for _game in _games:
            _gameParticipations = _gamesParticipations.filter(game=_game)
            setattr(_game, 'participants', _gameParticipations)
            setattr(_game, 'participants_count', _gameParticipations.count())

            _checkIfJoignable = True
            _checkIfQuitable = True
            try:
                if _game.status == GameStatus.FINISHED:
                    _checkIfJoignable = False
                    _checkIfQuitable = False

                _ = _gameParticipations.get(player=_executor)

                if _checkIfQuitable:
                    setattr(_game, 'is_quitable', True)

            except Participation.DoesNotExist:
                if _checkIfJoignable:
                    setattr(_game, 'is_joignable', True)

            _stages = _allStages.filter(game=_game)
            setattr(_game, 'stages', _stages)
            setattr(_game, 'stages_count', _stages.count())

        context['form_filter'] = _filterForm
        context['user_games'] = _games
        return context


class SignUpView(FormView):
    template_name = 'main/signup_form.html'
    form_class = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(SignUpView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):

        _user = User(username=form.cleaned_data.get('username'),
                     email=form.cleaned_data.get('email'),
                     first_name=form.cleaned_data.get('first_name'),
                     last_name=form.cleaned_data.get('last_name'))
        _user.set_password(form.cleaned_data.get('password'))
        _user.save()

        _msg = 'User account created successfully'
        print _msg
        messages.add_message(self.request, messages.SUCCESS, _msg)

        login(self.request, _user)
        _msg = 'User logged successfully'
        print _msg
        messages.add_message(self.request, messages.SUCCESS, _msg)

        return HttpResponseRedirect(reverse('user-profile'))

    def form_invalid(self, form):
        _msg = 'Error while creating user account : %s' % form.errors
        print _msg
        messages.add_message(self.request, messages.ERROR, mark_safe(_msg))
        return HttpResponseRedirect(reverse('auth-signup'))


class UserProfileView(LoginRequiredMixin, TemplateView, ViewHelper):
    template_name = 'main/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['form_fields'] = UserProfileForm(request=self.request)
        context['form_password'] = UserProfilePasswordChangeForm(request=self.request)
        return context

    def post(self, request, *args, **kwargs):
        _lp = '%s.post:' % self.__class__.__name__

        _executor = self.request.user
        print '%s self.request.POST : %s' % (_lp, self.request.POST)

        if self.request.POST.get('password_change'):
            # user modifies password

            _form = UserProfilePasswordChangeForm(self.request.POST, request=self.request)
            if not _form.is_valid():
                return self.return_error(self.request, 'Form is not valid', 'user-profile')

            _newPass = _form.cleaned_data.get('password')
            if _newPass != _form.cleaned_data.get('password_check'):
                return self.return_error(self.request, 'Passwords are different', 'user-profile')

            _executor.set_password(_newPass)
            _executor.save()
            login(request, _executor)
            return self.return_success(self.request, 'Password changed', 'user-profile')

        # user modifies other fields (email, first_name, last_name)
        _form = UserProfileForm(self.request.POST, request=self.request)
        if not _form.is_valid():
            return self.return_error(self.request, 'Form is not valid', 'user-profile')

        _pEmail = _form.cleaned_data.get('email')
        if _pEmail != _executor.email:
            _executor.email = _pEmail

        _pFirsName = _form.cleaned_data.get('first_name')
        if _pFirsName != _executor.first_name:
            _executor.first_name = _pFirsName

        _pLastName = _form.cleaned_data.get('last_name')
        if _pLastName != _executor.last_name:
            _executor.last_name = _pLastName

        _executor.save()

        return self.return_success(self.request, 'Profile changed', 'user-profile')
