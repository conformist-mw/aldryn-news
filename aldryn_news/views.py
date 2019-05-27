# -*- coding: utf-8 -*-
import datetime

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from menus.utils import set_language_changer

from aldryn_news import request_news_identifier
from aldryn_news.models import Category, News, Tag


class BaseNewsView(object):

    def get_queryset(self):
        if self.request.user.is_staff:
            manager = News.objects
        else:
            manager = News.published
        return manager.language()


class ArchiveView(BaseNewsView, ArchiveIndexView):

    model = News
    date_field = 'publication_start'
    allow_empty = True
    allow_future = True
    template_name = 'aldryn_news/news_list.html'
    date_list_period = 'month'

    def get_queryset(self):
        qs = super(ArchiveView, self).get_queryset()
        if 'month' in self.kwargs:
            qs = qs.filter(publication_start__month=self.kwargs['month'])
        if 'year' in self.kwargs:
            qs = qs.filter(publication_start__year=self.kwargs['year'])
        return qs

    def get_context_data(self, **kwargs):
        kwargs['month'] = int(self.kwargs.get('month')) if 'month' in self.kwargs else None
        kwargs['year'] = int(self.kwargs.get('year')) if 'year' in self.kwargs else None
        if kwargs['year']:
            kwargs['archive_date'] = datetime.date(kwargs['year'], kwargs['month'] or 1, 1)
        return super(ArchiveView, self).get_context_data(**kwargs)


class TaggedListView(BaseNewsView, ListView):

    template_name = 'aldryn_news/news_list.html'

    def get_queryset(self):
        qs = super(TaggedListView, self).get_queryset()
        # can't filter by tags (m2m) on TranslatedQuerySet
        tags = Tag.objects.filter(slug=self.kwargs['tag'])
        tagged = News.objects.filter(tags__id__in=tags)
        tagged_pks = list(tagged.values_list('pk', flat=True))
        return qs.filter(pk__in=tagged_pks)

    def get_context_data(self, **kwargs):
        kwargs['tagged_entries'] = (self.kwargs.get('tag')
                                    if 'tag' in self.kwargs else None)
        return super(TaggedListView, self).get_context_data(**kwargs)


class CategoryListView(BaseNewsView, ListView):

    template_name = 'aldryn_news/news_list.html'

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        response = super(CategoryListView, self).get(*args, **kwargs)
        set_language_changer(self.request, self.object.get_absolute_url)
        return response

    def get_object(self):
        return get_object_or_404(Category.objects.language(), slug=self.kwargs['category_slug'])

    def get_queryset(self):
        qs = super(CategoryListView, self).get_queryset()
        return qs.filter(category=self.object)


class NewsDetailView(BaseNewsView, DetailView):

    template_name = 'aldryn_news/news_detail.html'

    def get_object(self):
        # django-hvad 0.3.0 doesn't support Q conditions in `get` method
        # https://github.com/KristianOellegaard/django-hvad/issues/119
        qs = self.get_queryset()
        qs = qs.filter(slug=self.kwargs['slug'])
        if not qs.exists():
            raise Http404
        news = qs[0]
        setattr(self.request, request_news_identifier, news)
        return news

    def get(self, *args, **kwargs):
        response = super(NewsDetailView, self).get(*args, **kwargs)
        set_language_changer(self.request, self.object.get_absolute_url)
        return response
