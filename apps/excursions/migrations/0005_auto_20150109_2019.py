# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0004_excursion_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excursion',
            name='image',
        ),
        migrations.AlterField(
            model_name='excursion',
            name='img_preview',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=b'excursions_img_preview', blank=True),
        ),
    ]
