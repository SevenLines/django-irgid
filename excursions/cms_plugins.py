from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from excursions.models import Excursion


class ExcursionPlugin(CMSPluginBase):
    name = u"Excursion plugin"
    render_template = "excursions/excursion_item.html"
    text_enabled = True
    model = Excursion

    def render(self, context, instance, placeholder):
        prices_list = []
        price_lines = instance.priceList.splitlines()
        for p in price_lines:
            values = p.split('|', 1)
            prices_list.append((values[0].strip(' \t\n\r'), values[1].strip(' \t\n\r')))

        context['prices'] = prices_list
        context['time_length'] = instance.time_length / 60
        context['excursion'] = instance
        return context


plugin_pool.register_plugin(ExcursionPlugin)