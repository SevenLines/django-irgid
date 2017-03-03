# coding=utf-8
import calendar
from datetime import date, datetime

import re
from django.core.urlresolvers import reverse
from django.db import models, transaction
from django.db.models.signals import pre_delete, post_delete
from django.dispatch.dispatcher import receiver
from easy_thumbnails.fields import ThumbnailerImageField
from simple_history.models import HistoricalRecords

from excursions.managers import ExcursionsCategoryManager


class ExcursionCategory(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.TextField(default='')
    visible = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)
    image = ThumbnailerImageField(upload_to="excursions_category_img_preview", null=True, blank=True)

    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    objects = ExcursionsCategoryManager()

    history = HistoricalRecords()

    def __unicode__(self):
        return u"{title}|{id}".format(**self.__dict__)

    @property
    def is_gallery(self):
        return self.pk == ExcursionCategory.objects.get_gallery_id()

    @property
    def is_travel(self):
        return self.pk == ExcursionCategory.objects.get_travel_id()

    def get_excursions(self, request):
        if not request.user.is_authenticated():
            return Excursion.objects.filter(category=self, published=True)
        else:
            return Excursion.objects.filter(category=self)

    def get_absolute_url(self):
        return reverse("excursions.views.category", args=[self.pk])


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

    category = models.ForeignKey("ExcursionCategory", default=None, null=True)
    published = models.BooleanField("", default=False)

    history = HistoricalRecords()

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super(Excursion, self).save(force_insert, force_update, using, update_fields)

    def price_list_rendered(self):
        out = {
            'lines_count': 1,
            'data': []
        }
        min_price = None
        for_all = False
        price_lines = self.priceList.splitlines()
        for p in price_lines:
            values = p.split('|', 1)
            header = values[0].strip(' \t\n\r')
            data = values[1].strip(' \t\n\r').split('/')
            span = 0
            item = {
                'header': header,
                'default_price': data[0],
                'span': 0,
                'price_line': {
                    0: data[-1],  # взрослый
                    1: data[-2] if len(data) > 1 else data[-1],  # детский
                    2: data[-3] if len(data) > 2 else data[-1],  # дошкольный
                },
            }
            new_min_price = min(item['price_line'][0], item['price_line'][1], item['price_line'][2])
            new_min_price = re.sub("\D", "", new_min_price)
            new_min_price = int(new_min_price)
            min_price = min(new_min_price, min_price) if min_price else new_min_price
            if item['price_line'][0] == item['price_line'][1]:
                span = 2
                if item['price_line'][1] == item['price_line'][2]:
                    span = 3

            item['span'] = span
            out['data'].append(item)

            if len(data) > out['lines_count']:
                out['lines_count'] = len(data)
        out['lines'] = range(out['lines_count'])
        out['min_price'] = min_price
        return out

    def get_absolute_url(self):
        return reverse("excursions.views.excursion", args=[self.pk])

    def __unicode__(self):
        return u"{title}|{id}".format(**self.__dict__)


class ExcursionCalendar(models.Model):
    excursion = models.ForeignKey(Excursion, null=True, blank=True)
    date = models.DateField(default=date.today, unique=True)
    comment = models.TextField(default="")

    is_best = models.BooleanField(default=False, verbose_name='Является ли лучши предложением месяца')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        with transaction.atomic():
            if self.is_best:
                min_range, max_range = calendar.monthrange(date.today().year, date.today().month)
                min_range = date.today().replace(day=min_range)
                max_range = date.today().replace(day=max_range)
                # только одна главная экскурсия в месяц
                ExcursionCalendar.objects.filter(date__range=(min_range, max_range))\
                    .update(is_best=False)

            super(ExcursionCalendar, self).save(force_insert, force_update, using, update_fields)


class ExcursionAppointment(models.Model):
    full_name = models.CharField(max_length=256, null=False)
    phone = models.CharField(max_length=128, default="", blank=True)
    email = models.EmailField(default="", blank=True)
    comment = models.TextField(null=False, blank=False)

    create_date = models.DateTimeField(default=datetime.now, editable=False)
    update_date = models.DateTimeField(default=datetime.now)

    sended = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.update_date = datetime.now()
        super(ExcursionAppointment, self).save(force_insert, force_update, using, update_fields)


class ExcursionImage(models.Model):
    excursion = models.ForeignKey(Excursion, related_name='images')
    image = ThumbnailerImageField(upload_to="excursions_gallery")
    hidden = models.BooleanField(default=False)
    order = models.SmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']


@receiver(post_delete, sender=ExcursionImage)
def mymodel_delete(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)