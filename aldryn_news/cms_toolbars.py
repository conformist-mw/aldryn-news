# -*- coding: utf-8 -*-
from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from aldryn_news import request_news_identifier


@toolbar_pool.register
class NewsToolbar(CMSToolbar):

    def populate(self):
        def can(action, model):
            perm = 'aldryn_news.%(action)s_%(model)s' % {'action': action, 'model': model}
            return self.request.user.has_perm(perm)

        if self.is_current_app and (can('add', 'news') or can('change', 'news')):
            menu = self.toolbar.get_or_create_menu('news-app', _('News'))
            if can('add', 'news'):
                menu.add_modal_item(_('Add News'), reverse('admin:aldryn_news_news_add'))

            news = getattr(self.request, request_news_identifier, None)
            if news and can('change', 'news'):
                url = reverse('admin:aldryn_news_news_change', args=(news.pk,))
                menu.add_modal_item(_('Edit News'), url, active=True)
