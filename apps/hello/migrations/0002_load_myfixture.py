# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        from django.core.management import call_command
        call_command("loaddata", "initial.json")

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'hello.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'null': '1', 'blank': '1'}),
            'dob': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jabber': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'othercontacts': ('django.db.models.fields.TextField', [], {'null': '1', 'blank': '1'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': '1', 'blank': '1'})
        }
    }

    complete_apps = ['hello']
    symmetrical = True
