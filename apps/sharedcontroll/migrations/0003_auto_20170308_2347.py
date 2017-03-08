# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-08 15:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharedcontroll', '0002_auto_20170306_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedurl',
            name='service',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='sharedurl',
            name='url',
            field=models.URLField(default=b'', max_length=1000, null=True),
        ),
    ]
