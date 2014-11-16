from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.db.models import Model


class ExcursionClass(Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')


class Excursion(Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    length = models.IntegerField(verbose_name="way length in meters", blank=True, null=True)
    time_length = models.IntegerField(verbose_name="time takes in minutes", blank=True, null=True)
    priceList = models.TextField(verbose_name="price list", blank=True)
