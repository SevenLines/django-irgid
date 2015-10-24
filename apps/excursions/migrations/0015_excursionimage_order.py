# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0014_excursion_min_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursionimage',
            name='order',
            field=models.SmallIntegerField(default=0),
            preserve_default=True,
        ),
    ]
