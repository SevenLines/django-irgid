# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0023_auto_20160125_0304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursionappointment',
            name='email',
            field=models.EmailField(default=b'', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='excursionappointment',
            name='phone',
            field=models.CharField(default=b'', max_length=128, blank=True),
        ),
    ]
