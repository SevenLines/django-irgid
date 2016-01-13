# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_settings', '0007_historicalintegersetting_historicaltextsetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsetting',
            name='history_user',
        ),
        migrations.RemoveField(
            model_name='historicalsetting',
            name='polymorphic_ctype',
        ),
        migrations.DeleteModel(
            name='HistoricalSetting',
        ),
    ]
