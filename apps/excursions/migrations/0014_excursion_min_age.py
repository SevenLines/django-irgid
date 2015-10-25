# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0013_auto_20150122_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='min_age',
            field=models.SmallIntegerField(default=0, verbose_name=b'\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb2\xd0\xbe\xd0\xb7\xd1\x80\xd0\xb0\xd1\x81\xd1\x82'),
            preserve_default=True,
        ),
    ]
