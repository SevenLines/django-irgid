# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('custom_settings', '0004_auto_20151024_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_custom_settings.setting_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
