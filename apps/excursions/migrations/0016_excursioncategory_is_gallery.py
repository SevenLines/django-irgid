# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0015_excursionimage_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursioncategory',
            name='is_gallery',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
