# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0022_excursionappointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursionappointment',
            name='full_name',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='excursionappointment',
            name='email',
            field=models.EmailField(default=b'', max_length=254),
        ),
        migrations.AlterField(
            model_name='excursionappointment',
            name='phone',
            field=models.CharField(default=b'', max_length=128),
        ),
    ]
