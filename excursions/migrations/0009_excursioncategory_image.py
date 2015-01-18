# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0008_excursioncategory_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='excursioncategory',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(null=True, upload_to=b'excursions_category_img_preview', blank=True),
            preserve_default=True,
        ),
    ]
