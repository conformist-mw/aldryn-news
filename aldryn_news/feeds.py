# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from aldryn_news.models import Category, News

LATEST_ENTRIES = 10


class LatestEntriesFeed(Feed):

    def link(self):
        return reverse('latest-news', current_app='news')

    def title(self):
        return _('News on %(site_name)s') % {'site_name': Site.objects.get_current().name}

    def items(self, obj):
        return News.published.language().order_by('-publication_start')[:LATEST_ENTRIES]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead_in


class TagFeed(LatestEntriesFeed):

    def get_object(self, request, tag):
        return tag

    def items(self, obj):
        # can't filter by tags on TranslatedQuerySet
        tagged_pks = list(News.published.filter(tags__slug=obj).values_list('pk', flat=True))
        return News.published.language().filter(pk__in=tagged_pks)[:LATEST_ENTRIES]


class CategoryFeed(LatestEntriesFeed):

    def get_object(self, request, slug):
        return get_object_or_404(Category.objects.language(), slug=slug)

    def items(self, obj):
        return News.published.language().filter(category=obj)[:LATEST_ENTRIES]
