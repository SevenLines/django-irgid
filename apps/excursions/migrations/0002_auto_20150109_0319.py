# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0001_initial'),
        ('excursions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='image',
            field=filer.fields.image.FilerImageField(related_name=b'excursion_images', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='excursion',
            name='img_preview',
            field=filer.fields.image.FilerImageField(related_name=b'small_preview', blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
    ]
