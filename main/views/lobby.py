# -*- coding: utf-8 -*-
from django.core.paginator import Paginator

from ..core.const.lobby.rallies import RallyStatus
from ..forms.lobby import FilterRalliesForm, PaginationPageSizeForm
from ..generic.views import MainTemplateView
from ..models import Rally, Participation, Stage


class LobbyView(MainTemplateView):
    template_name = 'main/lobby.html'

    def __init__(self, *args, **kwargs):
        super(LobbyView, self).__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        self.log.startView(_executor)

        context = super(LobbyView, self).get_context_data(**kwargs)
        context['ariane'] = ['lobby']

        _pgPageSize = int(self.request.GET.get('_pgps', 10))
        _pgPageIndex = int(self.request.GET.get('_pgpi', 1))
        _allRlys = Rally.objects.all()

        # prepare filters
        _form = FilterRalliesForm(request=self.request)
        _orderBy = _form.fields['ord_b'].initial
        _orderWay = _form.fields['ord_w'].initial
        _userPart = _form.fields['usr_part'].initial
        _rallyStatus = _form.fields['rly_stat'].initial
        _rallyCreator = _form.fields['rly_crea'].initial
        _ralliesFilter = dict()
        _ralliesExclude = dict()

        # manage creator filter
        if _rallyCreator == 'me':
            _ralliesFilter['creator'] = _executor
        elif _rallyCreator == 'nm':
            _ralliesExclude['creator'] = _executor

        # manage rally status filter
        if _rallyStatus not in ['-', '']:
            _ralliesFilter['status'] = _rallyStatus

        # apply filters
        _rallies = _allRlys.exclude(**_ralliesExclude).filter(**_ralliesFilter)

        # manage user_participation
        _rlysParts = Participation.objects.filter(rally__in=_rallies)

        _rlyUserParts = _rlysParts.filter(player=_executor)
        _rlysUserPartsIds = _rlyUserParts.values_list('rally__id', flat=True)
        if not _executor.is_anonymous:
            if _userPart == '1':
                _rallies = _rallies.filter(id__in=_rlysUserPartsIds)
            elif _userPart == '0':
                _rallies = _rallies.exclude(id__in=_rlysUserPartsIds)

        # order by database fields
        if _orderBy and _orderBy in ['label', 'status', 'creator', 'created_at', 'opened_at']:
            _rallies = _rallies.order_by('%s%s' % ('-' if _orderWay == 'd' else '', _orderBy))

        # prepare pagination page size
        data_dict = {'available_page_sizes': _pgPageSize,
                     'selected_page_size': _pgPageSize}
        context['form_pgps'] = PaginationPageSizeForm(initial=data_dict)

        context['rallies_total'] = _rallies.count()

        # select rallies of current pagination
        paginator = Paginator(_rallies, _pgPageSize)
        try:
            _rallies = paginator.page(_pgPageIndex)
        except Exception as e:
            _msg = 'Error while retrieving a page of the paginator : %s' % (repr(e))
            return self.set_context_error(self.request, _msg, context)

        # browse elected rally, and add temporary attributes
        _allStages = Stage.objects.all()
        for _rally in _rallies:
            _rlyParts = _rlysParts.filter(rally=_rally)
            setattr(_rally, 'participants', _rlyParts)
            setattr(_rally, 'participants_count', _rlyParts.count())

            _checkIfJoignable = True
            _checkIfQuitable = True
            _checkIfDeletable = True
            try:

                if _rally.status in [RallyStatus.SCHEDULED, RallyStatus.STARTED, RallyStatus.FINISHED]:
                    _checkIfJoignable = False

                if _rally.status in [RallyStatus.STARTED, RallyStatus.FINISHED]:
                    _checkIfQuitable = False

                if _rally.status in [RallyStatus.STARTED, RallyStatus.FINISHED]:
                    _checkIfDeletable = False

                if _executor.is_anonymous:
                    raise Participation.DoesNotExist

                _ = _rlyParts.get(player=_executor)

                setattr(_rally, 'is_quitable', _checkIfQuitable)

            except Participation.DoesNotExist:
                setattr(_rally, 'is_joignable', _checkIfJoignable)

            setattr(_rally, 'is_deletable', _checkIfDeletable)

            _stages = _allStages.filter(rally=_rally)
            setattr(_rally, 'stages', _stages)
            setattr(_rally, 'stages_count', _stages.count())

        # order by
        if _orderBy and _orderBy in ['number_of_participants', 'number_of_ss']:
            # todo : manage ordering by logic data
            pass

        context['pgps'] = _pgPageSize

        context['form_filter'] = _form
        context['rallies'] = _rallies
        context['pages_list'] = self.get_pages_list(_pgPageIndex, paginator.num_pages)

        url = self.request.get_full_path()

        # calculates if a filter other than the navigation filter is used
        url = url.replace('?_pgpi=%s' % _pgPageIndex, '')
        url = url.replace('&_pgpi=%s' % _pgPageIndex, '')
        url = url.replace('?_pgps=%s' % _pgPageSize, '')
        url = url.replace('&_pgps=%s' % _pgPageSize, '')
        context['has_filter'] = True if url.find('?') > 0 else False

        context['page_url'] = url

        self.log.endView()
        return context

    @classmethod
    def get_pages_list(cls, num_page, page_count):
        # prepare pagin list of pages
        pages_list = list()

        if page_count > 7:
            # slot 1
            pages_list.append(1)

            # slot 2
            if num_page <= 4:
                pages_list.append(2)
            else:
                pages_list.append(0)

            # slot 3
            if num_page <= 4:
                pages_list.append(3)
            elif num_page == 5:
                pages_list.append(4)
            elif num_page > (page_count - 4):
                pages_list.append(page_count - 4)
            else:
                pages_list.append(num_page - 1)

            # slot 4
            if num_page <= 4:
                pages_list.append(4)
            elif num_page >= (page_count - 3):
                pages_list.append(page_count - 3)
            else:
                pages_list.append(num_page)

            # slot 5
            if num_page <= 4:
                pages_list.append(5)
            elif num_page >= (page_count - 2):
                pages_list.append(page_count - 2)
            else:
                pages_list.append(num_page + 1)

            # slot 6
            if num_page >= (page_count - 3):
                pages_list.append(page_count - 1)
            else:
                pages_list.append(0)

            # slot 7
            pages_list.append(page_count)
        else:

            pages_list = [index for index in range(1, page_count + 1)]

        return pages_list
