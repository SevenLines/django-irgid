# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('excursions', '0018_auto_20151114_1026'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcursionCalendar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('comment', models.TextField(default=b'')),
                ('is_best', models.BooleanField(default=False, verbose_name=b'\xd0\xaf\xd0\xb2\xd0\xbb\xd1\x8f\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xbb\xd0\xb8 \xd0\xbb\xd1\x83\xd1\x87\xd1\x88\xd0\xb8 \xd0\xbc\xd0\xbf\xd1\x80\xd0\xb5\xd0\xb4\xd0\xbb\xd0\xbe\xd0\xb6\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5\xd0\xbc \xd0\xbc\xd0\xb5\xd1\x81\xd1\x8f\xd1\x86\xd0\xb0')),
                ('excursion', models.ForeignKey(blank=True, to='excursions.Excursion', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalExcursion',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default=b'')),
                ('short_description', models.TextField(default=b'')),
                ('length', models.IntegerField(default=0, verbose_name=b'way length in meters')),
                ('time_length', models.IntegerField(default=0, verbose_name=b'time takes in minutes')),
                ('min_age', models.SmallIntegerField(default=0, verbose_name=b'\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd1\x8b\xd0\xb9 \xd0\xb2\xd0\xbe\xd0\xb7\xd1\x80\xd0\xb0\xd1\x81\xd1\x82')),
                ('priceList', models.TextField(default=b'', verbose_name=b'price list')),
                ('yandex_map_script', models.TextField(default=b'')),
                ('update_date', models.DateTimeField(editable=False, blank=True)),
                ('create_date', models.DateTimeField(editable=False, blank=True)),
                ('img_preview', models.TextField(max_length=100, null=True, blank=True)),
                ('published', models.BooleanField(default=False, verbose_name=b'')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('category', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='excursions.ExcursionCategory', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical excursion',
            },
        ),
        migrations.CreateModel(
            name='HistoricalExcursionCategory',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'')),
                ('visible', models.BooleanField(default=False)),
                ('order', models.SmallIntegerField(default=0)),
                ('image', models.TextField(max_length=100, null=True, blank=True)),
                ('update_date', models.DateTimeField(editable=False, blank=True)),
                ('create_date', models.DateTimeField(editable=False, blank=True)),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical excursion category',
            },
        ),
        migrations.AlterField(
            model_name='excursionimage',
            name='excursion',
            field=models.ForeignKey(related_name='images', to='excursions.Excursion'),
        ),
    ]
