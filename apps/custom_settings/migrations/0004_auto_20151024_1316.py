# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_settings', '0003_integersetting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integersetting',
            name='value',
            field=models.IntegerField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='textsetting',
            name='value',
            field=models.TextField(default=True, null=True),
        ),
    ]
