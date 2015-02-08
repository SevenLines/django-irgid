# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('textpage', '0003_textpageimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textpageimage',
            name='image',
            field=easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'textpage'),
            preserve_default=True,
        ),
    ]
