# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0002_auto_20150109_0319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excursion',
            name='image',
        ),
        migrations.AlterField(
            model_name='excursion',
            name='img_preview',
            field=models.ImageField(null=True, upload_to=b'excursions_img_preview', blank=True),
        ),
    ]
