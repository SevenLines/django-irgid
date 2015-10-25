# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0012_auto_20150119_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='excursioncategory',
            name='visible',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
