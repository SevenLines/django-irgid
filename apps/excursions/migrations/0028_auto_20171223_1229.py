# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-23 04:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0027_auto_20171104_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursion',
            name='description_en',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursion',
            name='description_ru',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursion',
            name='published_en',
            field=models.BooleanField(default=False, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='excursion',
            name='published_ru',
            field=models.BooleanField(default=False, verbose_name=b''),
        ),
        migrations.AddField(
            model_name='excursion',
            name='short_description_en',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursion',
            name='short_description_ru',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursion',
            name='title_en',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='excursion',
            name='title_ru',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='description_en',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='description_ru',
            field=models.TextField(default=b'', null=True),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='title_en',
            field=models.CharField(default=b'', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='title_ru',
            field=models.CharField(default=b'', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='visible_en',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='excursioncategory',
            name='visible_ru',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalexcursion',
            name='history_type',
            field=models.CharField(choices=[('+', '\u0421\u043e\u0437\u0434\u0430\u043d'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1),
        ),
        migrations.AlterField(
            model_name='historicalexcursioncategory',
            name='history_type',
            field=models.CharField(choices=[('+', '\u0421\u043e\u0437\u0434\u0430\u043d'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1),
        ),
    ]
