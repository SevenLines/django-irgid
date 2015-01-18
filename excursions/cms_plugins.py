from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from excursions.models import Excursion, ExcursionCategoryPluginModel


class ExcursionCategoryPlugin(CMSPluginBase):
    name = u"Excursion category plugin"
    render_template = "excursions/category/description-category.html"
    text_enabled = False
    model = ExcursionCategoryPluginModel
    cache = False

    def render(self, context, instance, placeholder):
        context['excursions'] = instance.category.excursions(context['request'])
        context['current_category'] = instance.category
        return context

plugin_pool.register_plugin(ExcursionCategoryPlugin)