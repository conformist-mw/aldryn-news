# -*- coding: utf-8 -*-
from aldryn_search.utils import get_index_base, strip_tags
from cms.plugin_rendering import ContentRenderer
from django.conf import settings
from sekizai.context import SekizaiContext

from aldryn_news.models import News


def render_plugin(request, plugin_instance):
    renderer = ContentRenderer(request)
    context = SekizaiContext(request)
    context['request'] = request
    return renderer.render_plugin(plugin_instance, context)


class NewsIndex(get_index_base()):
    haystack_use_for_indexing = getattr(settings, "ALDRYN_NEWS_SEARCH", True)

    INDEX_TITLE = True  # for backward compatibility until 1.1.0 aldryn-search
    index_title = True

    def get_title(self, obj):
        return obj.title

    def get_index_kwargs(self, language):
        return {'translations__language_code': language}

    def get_index_queryset(self, language):
        return self.get_model().published.all()

    def get_model(self):
        return News

    def get_search_data(self, obj, language, request):
        text_bits = [strip_tags(obj.lead_in)]
        plugins = obj.content.cmsplugin_set.filter(language=language)
        for base_plugin in plugins:
            plugin_instance, plugin_type = base_plugin.get_plugin_instance()
            if plugin_instance is not None:
                plugin_contents = strip_tags(render_plugin(request, plugin_instance))
                text_bits.append(plugin_contents)

        return ' '.join(text_bits)
