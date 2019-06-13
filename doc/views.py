# -*- coding: utf-8 -*-
import markdown2

from django.views.generic import TemplateView

from rallyman import settings

from . import utils


class DocPageView(TemplateView):
    template_name = 'doc/doc.html'

    def get_context_data(self, **kwargs):
        _executor = self.request.user
        _pageKey = kwargs.get('pk', utils.DocPages.getDefaultPageConfiguration()['key'])
        context = super(DocPageView, self).get_context_data(**kwargs)
        context['ariane'] = ['about', 'doc', _pageKey]

        _pageConf = utils.DocPages.getPageConfiguration(_pageKey)

        _mdFilePath = '%s\\doc\\%s' % (settings.BASE_DIR, _pageConf['filepath'])
        _htmlDoc = markdown2.markdown_path(_mdFilePath)

        context['doc_pages'] = utils.DocPages.getPagesConfiguration(_executor)
        context['page_title'] = _pageConf['title']
        context['page_content'] = _htmlDoc
        return context
