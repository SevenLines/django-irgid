# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 12:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0025_excursioncalendar_comment_rendered'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='popular',
            field=models.BooleanField(default=False, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='historicalexcursion',
            name='popular',
            field=models.BooleanField(default=False, verbose_name=b''),
        ),
    ]
