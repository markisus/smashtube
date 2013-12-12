# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'smashgames_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'smashgames', ['Player'])

        # Adding M2M table for field mains on 'Player'
        m2m_table_name = db.shorten_name(u'smashgames_player_mains')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('player', models.ForeignKey(orm[u'smashgames.player'], null=False)),
            ('character', models.ForeignKey(orm[u'smashdata.character'], null=False))
        ))
        db.create_unique(m2m_table_name, ['player_id', 'character_id'])

        # Adding model 'Tournament'
        db.create_table(u'smashgames_tournament', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'smashgames', ['Tournament'])

        # Adding model 'Section'
        db.create_table(u'smashgames_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'smashgames', ['Section'])

        # Adding model 'Set'
        db.create_table(u'smashgames_set', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashdata.GameInfo'])),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashgames.Tournament'], null=True, blank=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashgames.Section'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'smashgames', ['Set'])

        # Adding model 'Match'
        db.create_table(u'smashgames_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1, blank=True)),
            ('set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashgames.Set'], null=True, blank=True)),
            ('video_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('end', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal(u'smashgames', ['Match'])

        # Adding model 'PlayerSession'
        db.create_table(u'smashgames_playersession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashgames.Player'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashgames.Match'])),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['smashdata.Character'])),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('index', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'smashgames', ['PlayerSession'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'smashgames_player')

        # Removing M2M table for field mains on 'Player'
        db.delete_table(db.shorten_name(u'smashgames_player_mains'))

        # Deleting model 'Tournament'
        db.delete_table(u'smashgames_tournament')

        # Deleting model 'Section'
        db.delete_table(u'smashgames_section')

        # Deleting model 'Set'
        db.delete_table(u'smashgames_set')

        # Deleting model 'Match'
        db.delete_table(u'smashgames_match')

        # Deleting model 'PlayerSession'
        db.delete_table(u'smashgames_playersession')


    models = {
        u'smashdata.character': {
            'Meta': {'object_name': 'Character'},
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['smashdata.GameInfo']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'smashdata.gameinfo': {
            'Meta': {'object_name': 'GameInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '70'})
        },
        u'smashgames.match': {
            'Meta': {'object_name': 'Match'},
            'end': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'blank': 'True'}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['smashgames.Player']", 'through': u"orm['smashgames.PlayerSession']", 'symmetrical': 'False'}),
            'set': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashgames.Set']", 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'video_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'smashgames.player': {
            'Meta': {'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mains': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['smashdata.Character']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'smashgames.playersession': {
            'Meta': {'object_name': 'PlayerSession'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashdata.Character']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashgames.Match']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashgames.Player']"}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'})
        },
        u'smashgames.section': {
            'Meta': {'object_name': 'Section'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'smashgames.set': {
            'Meta': {'object_name': 'Set'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashdata.GameInfo']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashgames.Section']", 'null': 'True', 'blank': 'True'}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['smashgames.Tournament']", 'null': 'True', 'blank': 'True'})
        },
        u'smashgames.tournament': {
            'Meta': {'object_name': 'Tournament'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['smashgames']