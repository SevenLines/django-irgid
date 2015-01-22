# coding=utf-8
from cms.models.pluginmodel import CMSPlugin
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Model
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from easy_thumbnails.fields import ThumbnailerImageField


class ExcursionCategory(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    visible = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)
    image = ThumbnailerImageField(upload_to="excursions_category_img_preview", null=True, blank=True)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    def excursions(self, request):
        if not request.user.is_authenticated():
            return Excursion.objects.filter(category=self, published=True)
        else:
            return Excursion.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse("excursions.views.category", args=[self.pk])


class ExcursionCategoryPluginModel(CMSPlugin):
    category = models.ForeignKey("ExcursionCategory")

    def __unicode__(self):
        return self.category.title if self.category else ""


class Excursion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default="")
    short_description = models.TextField(default="")
    length = models.IntegerField(verbose_name="way length in meters", default=0)
    time_length = models.IntegerField(verbose_name="time takes in minutes", default=0)
    min_age = models.SmallIntegerField(verbose_name="минимальный возраст", default=0)
    priceList = models.TextField(verbose_name="price list", default="")
    yandex_map_script = models.TextField(default="")

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

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

    def get_absolute_url(self):
        return reverse("excursions.views.excursion", args=[self.pk])


class ExcursionImage(models.Model):
    excursion = models.ForeignKey(Excursion)
    image = ThumbnailerImageField(upload_to="excursions_gallery")
    actve = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)


@receiver(post_delete, sender=ExcursionImage)
def mymodel_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)