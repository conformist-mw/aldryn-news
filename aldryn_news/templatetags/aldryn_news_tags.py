# -*- coding: utf-8 -*-
from cms.utils import get_language_from_request
from django import template
from django.conf import settings
from django.utils.translation import get_language

from aldryn_news.models import News

register = template.Library()


def get_language_from_context(context):
    if 'LANGUAGE_CODE' in context:
        return context['LANGUAGE_CODE']
    elif 'request' in context:
        return get_language_from_request(context['request'])
    else:
        return get_language() or settings.LANGUAGE_CODE


@register.simple_tag(name='news_tags', takes_context=True)
def get_news_tags(context, news_ids):
    if news_ids:
        current_language = get_language_from_context(context)
        # We assume if it has no ok attribute then it's a pk :(
        get_pk = lambda instance: getattr(instance, 'pk', instance)
        news_ids = [get_pk(news) for news in news_ids]
        news_tags = News.published.get_tags(language=current_language, news_ids=news_ids)
        return news_tags
    return ''
