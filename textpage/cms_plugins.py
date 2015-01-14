from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from textpage.models import TextPage


class TextPagePlugin(CMSPluginBase):
    name = "textpage"
    render_template = "textpage/page.html"
    model = TextPage
    cache = False


plugin_pool.register_plugin(TextPagePlugin)