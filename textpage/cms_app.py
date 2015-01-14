from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

__author__ = 'm'

class TextPageHook(CMSApp):
    name = 'textpage'
    urls = ["textpage.urls"]

apphook_pool.register(TextPageHook)