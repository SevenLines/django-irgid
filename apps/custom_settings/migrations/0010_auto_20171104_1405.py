# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-04 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_settings', '0009_auto_20170303_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalintegersetting',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='historicaltextsetting',
            name='history_change_reason',
            field=models.CharField(max_length=100, null=True),
        ),
    ]