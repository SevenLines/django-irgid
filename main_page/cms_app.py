from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class MainPage(CMSApp):
    name = "main page"
    urls = ["main_page.urls"]

apphook_pool.register(MainPage)