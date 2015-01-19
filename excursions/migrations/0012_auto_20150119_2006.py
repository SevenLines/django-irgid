# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0011_excursioncategorypluginmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 12, 6, 11, 645737, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='excursion',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 12, 6, 18, 686182, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 12, 6, 29, 703035, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 19, 12, 6, 35, 648676, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
