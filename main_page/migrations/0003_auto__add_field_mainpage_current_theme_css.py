# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MainPage.current_theme_css'
        db.add_column(u'main_page_mainpage', 'current_theme_css',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MainPage.current_theme_css'
        db.delete_column(u'main_page_mainpage', 'current_theme_css')


    models = {
        u'main_page.mainpage': {
            'Meta': {'object_name': 'MainPage'},
            'current_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main_page.MainPageItem']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
            'current_theme_css': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_border': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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