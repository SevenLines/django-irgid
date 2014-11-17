# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MainPageItem'
        db.create_table(u'main_page_mainpageitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main_page', ['MainPageItem'])

        # Adding model 'MainPage'
        db.create_table(u'main_page_mainpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('current_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main_page.MainPageItem'], null=True, on_delete=models.SET_NULL)),
        ))
        db.send_create_signal(u'main_page', ['MainPage'])


    def backwards(self, orm):
        # Deleting model 'MainPageItem'
        db.delete_table(u'main_page_mainpageitem')

        # Deleting model 'MainPage'
        db.delete_table(u'main_page_mainpage')


    models = {
        u'main_page.mainpage': {
            'Meta': {'object_name': 'MainPage'},
            'current_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_page.MainPageItem']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main_page.mainpageitem': {
            'Meta': {'object_name': 'MainPageItem'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['main_page']