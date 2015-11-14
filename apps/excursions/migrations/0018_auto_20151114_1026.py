# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0017_remove_excursioncategory_is_gallery'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excursionimage',
            options={'ordering': ['order', 'id']},
        ),
        migrations.RenameField(
            model_name='excursionimage',
            old_name='actve',
            new_name='hidden',
        ),
    ]
