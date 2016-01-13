# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0019_auto_20151210_0455'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursioncalendar',
            name='month',
            field=models.SmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='excursioncalendar',
            name='year',
            field=models.SmallIntegerField(default=2016),
        ),
        migrations.AlterField(
            model_name='excursioncalendar',
            name='is_best',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\xaf\xd0\xb2\xd0\xbb\xd1\x8f\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xbb\xd0\xb8 \xd0\xbb\xd1\x83\xd1\x87\xd1\x88\xd0\xb8 \xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5\xd0\xbc \xd0\xbc\xd0\xb5\xd1\x81\xd1\x8f\xd1\x86\xd0\xb0'),
        ),
    ]
