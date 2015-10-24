# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Excursion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(default=b'')),
                ('short_description', models.TextField(default=b'')),
                ('length', models.IntegerField(default=0, verbose_name=b'way length in meters')),
                ('time_length', models.IntegerField(default=0, verbose_name=b'time takes in minutes')),
                ('priceList', models.TextField(default=b'', verbose_name=b'price list')),
                ('published', models.BooleanField(default=False, verbose_name=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExcursionCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='excursion',
            name='category',
            field=models.ForeignKey(default=None, to='excursions.ExcursionCategory', null=True),
            preserve_default=True,
        ),
    ]
