# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0007_excursion_yandex_map_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursioncategory',
            name='order',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
