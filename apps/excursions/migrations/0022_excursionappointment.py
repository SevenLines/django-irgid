# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0021_auto_20160113_0758'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcursionAppointment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.TextField()),
                ('create_date', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('update_date', models.DateTimeField(default=datetime.datetime.now)),
                ('sended', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
