# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_settings', '0002_setting_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegerSetting',
            fields=[
                ('setting_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='custom_settings.Setting')),
                ('value', models.IntegerField()),
            ],
            bases=('custom_settings.setting',),
        ),
    ]
