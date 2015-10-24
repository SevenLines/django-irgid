# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0016_excursioncategory_is_gallery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excursioncategory',
            name='is_gallery',
        ),
    ]
