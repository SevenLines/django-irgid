# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0009_excursioncategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursioncategory',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
