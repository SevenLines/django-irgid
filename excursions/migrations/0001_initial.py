# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExcursionCategory'
        db.create_table(u'excursions_excursioncategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'excursions', ['ExcursionCategory'])

        # Adding model 'Excursion'
        db.create_table(u'excursions_excursion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time_length', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('priceList', self.gf('django.db.models.fields.TextField')(default='')),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['excursions.ExcursionCategory'], null=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'excursions', ['Excursion'])


    def backwards(self, orm):
        # Deleting model 'ExcursionCategory'
        db.delete_table(u'excursions_excursioncategory')

        # Deleting model 'Excursion'
        db.delete_table(u'excursions_excursion')


    models = {
        u'excursions.excursion': {
            'Meta': {'object_name': 'Excursion'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['excursions.ExcursionCategory']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'priceList': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'time_length': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'excursions.excursioncategory': {
            'Meta': {'object_name': 'ExcursionCategory'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['excursions']