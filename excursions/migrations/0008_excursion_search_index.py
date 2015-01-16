# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgfulltext.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0007_excursion_yandex_map_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='search_index',
            field=djorm_pgfulltext.fields.VectorField(default=b'', serialize=False, null=True, editable=False, db_index=True),
            preserve_default=True,
        ),
    ]
