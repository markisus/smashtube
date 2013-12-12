# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GameInfo'
        db.create_table(u'smashdata_gameinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=70)),
        ))
        db.send_create_signal(u'smashdata', ['GameInfo'])

        # Adding model 'Character'
        db.create_table(u'smashdata_character', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'smashdata', ['Character'])

        # Adding M2M table for field games on 'Character'
        m2m_table_name = db.shorten_name(u'smashdata_character_games')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('character', models.ForeignKey(orm[u'smashdata.character'], null=False)),
            ('gameinfo', models.ForeignKey(orm[u'smashdata.gameinfo'], null=False))
        ))
        db.create_unique(m2m_table_name, ['character_id', 'gameinfo_id'])

        # Adding model 'CharacterIcon'
        db.create_table(u'smashdata_charactericon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashdata.Character'])),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashdata.GameInfo'])),
        ))
        db.send_create_signal(u'smashdata', ['CharacterIcon'])


    def backwards(self, orm):
        # Deleting model 'GameInfo'
        db.delete_table(u'smashdata_gameinfo')

        # Deleting model 'Character'
        db.delete_table(u'smashdata_character')

        # Removing M2M table for field games on 'Character'
        db.delete_table(db.shorten_name(u'smashdata_character_games'))

        # Deleting model 'CharacterIcon'
        db.delete_table(u'smashdata_charactericon')


    models = {
        u'smashdata.character': {
            'Meta': {'object_name': 'Character'},
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['smashdata.GameInfo']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'smashdata.charactericon': {
            'Meta': {'object_name': 'CharacterIcon'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashdata.Character']"}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashdata.GameInfo']"}),
            'icon': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'smashdata.gameinfo': {
            'Meta': {'object_name': 'GameInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        }
    }

    complete_apps = ['smashdata']