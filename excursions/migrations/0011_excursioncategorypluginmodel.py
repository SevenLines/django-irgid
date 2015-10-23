# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        # ('cms', '0003_auto_20140926_2347'),
        ('excursions', '0010_excursioncategory_visible'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcursionCategoryPluginModel',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('category', models.ForeignKey(to='excursions.ExcursionCategory')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
