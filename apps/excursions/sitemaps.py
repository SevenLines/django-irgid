from datetime import timedelta
from django.contrib.sitemaps import Sitemap
from django.db.models import Q, Min, Max
from django.urls.base import reverse

from excursions.models import Excursion, ExcursionCategory, ExcursionCalendar


class ExcursionsSitemap(Sitemap):
    changefreq = 'weekly'

    def get_items(self):
        return Excursion.objects.filter(
            published=True,
            category__isnull=False
        ).select_related("category")

    def items(self):
        out = []
        for item in self.get_items():
            if item.category.visible and not (item.category.is_gallery or item.category.is_travel):
                out.append(item)
        return out

    def lastmod(self, obj):
        return obj.update_date


class ExcursionsCategorySitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ExcursionCategory.objects.common_with_all(None)

    def lastmod(self, obj):
        return obj.update_date


class ExcursionsTravelSitemap(ExcursionsSitemap):
    def items(self):
        out = []
        for item in self.get_items():
            if item.category.is_travel:
                out.append(item)
        return out

    def location(self, obj):
        return reverse("travel:item", args=[obj.id, obj.title])


class ExcursionsGallerySitemap(ExcursionsSitemap):
    def items(self):
        out = []
        for item in self.get_items():
            if item.category.is_gallery:
                out.append(item)
        return out

    def location(self, obj):
        return reverse("gallery:item", args=[obj.id, obj.title])


# class CalendarSitemap(Sitemap):
#     def items(self):
#         date_range = ExcursionCalendar.objects.aggregate(
#             min_date=Min('date'), max_date=Max('date')
#         )
#
#         delta = date_range['max_date'] - date_range['min_date']
#
#         dates = {(d.year, d.month) for d in
#                  [date_range['min_date'] + timedelta(dlt) for dlt in range(delta + 1)]}
#
#         return dates
#
#     def location(self, (year, month)):
#         return reverse("excursions:calendar")


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['index', 'about', 'confedential', 'faq']

    def location(self, item):
        return reverse(item)


class CalendarSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return ['excursions:calendar']

    def location(self, item):
        return reverse(item)