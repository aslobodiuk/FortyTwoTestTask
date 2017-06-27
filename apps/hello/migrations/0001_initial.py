# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'hello_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dob', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=1, blank=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('jabber', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('skype', self.gf('django.db.models.fields.CharField')(max_length=50, null=1, blank=1)),
            ('othercontacts', self.gf('django.db.models.fields.TextField')(null=1, blank=1)),
        ))
        db.send_create_signal(u'hello', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'hello_person')


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