from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.db.models import Model


class ExcursionCategory(Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')

    def excursions(self, request):
        if not request.user.is_authenticated():
            return Excursion.objects.filter(category=self, published=True)
        else:
            return Excursion.objects.filter(category=self)


class Excursion(Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    short_description = models.TextField(default="")
    length = models.IntegerField(verbose_name="way length in meters", default=0)
    time_length = models.IntegerField(verbose_name="time takes in minutes", default=0)
    priceList = models.TextField(verbose_name="price list", default="")

    # img_preview = models.ImageField(upload_to="excursions_previews", default=None)

    category = models.ForeignKey("ExcursionCategory", default=None, null=True)
    published = models.BooleanField("", default=False)

    @property
    def price_list_rendered(self):
        out = []
        price_lines = self.priceList.splitlines()
        for p in price_lines:
            values = p.split('|', 1)
            out.append((values[0].strip(' \t\n\r'), values[1].strip(' \t\n\r')))
        return out