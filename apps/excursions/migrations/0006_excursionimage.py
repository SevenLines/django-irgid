# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0005_auto_20150109_2019'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcursionImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'excursions_gallery')),
                ('actve', models.BooleanField(default=False)),
                ('excursion', models.ForeignKey(to='excursions.Excursion')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
