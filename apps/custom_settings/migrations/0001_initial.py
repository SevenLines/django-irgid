# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(unique=True, max_length=128, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextSetting',
            fields=[
                ('setting_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='custom_settings.Setting')),
                ('value', models.TextField()),
            ],
            options={
            },
            bases=('custom_settings.setting',),
        ),
    ]
