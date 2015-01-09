from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.db.models import Model
from easy_thumbnails.fields import ThumbnailerImageField
from filer.fields.image import FilerImageField


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

    img_preview = ThumbnailerImageField(upload_to="excursions_img_preview", null=True, blank=True)
    # image = models.ThumbnailerImageField(upload_to="excursions_big_img_preview", null=True, blank=True)

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