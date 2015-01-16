# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0006_excursionimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='yandex_map_script',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
