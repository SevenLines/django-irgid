# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0020_auto_20160104_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excursioncalendar',
            name='month',
        ),
        migrations.RemoveField(
            model_name='excursioncalendar',
            name='year',
        ),
        migrations.AlterField(
            model_name='excursioncalendar',
            name='date',
            field=models.DateField(default=datetime.date.today, unique=True),
        ),
    ]
