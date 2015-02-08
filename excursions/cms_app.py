from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

__author__ = 'm'


class ExcursionsHook(CMSApp):
    name = 'excursion'
    urls = ["excursions.urls.excursions"]


class ExcursionsGalleryHook(CMSApp):
    name = 'excursion-gallery'
    urls = ["excursions.urls.gallery"]


apphook_pool.register(ExcursionsHook)
apphook_pool.register(ExcursionsGalleryHook)