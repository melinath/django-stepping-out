# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Venue'
        db.delete_table(u'stepping_out_venue')

        # Deleting field 'Lesson.venue'
        db.delete_column(u'stepping_out_lesson', 'venue_id')

        # Deleting field 'Dance.venue'
        db.delete_column(u'stepping_out_dance', 'venue_id')

        # Deleting field 'DanceTemplate.venue'
        db.delete_column(u'stepping_out_dancetemplate', 'venue_id')

        # Deleting field 'LessonTemplate.venue'
        db.delete_column(u'stepping_out_lessontemplate', 'venue_id')


    def backwards(self, orm):
        # Adding model 'Venue'
        db.create_table(u'stepping_out_venue', (
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('custom_map_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('banner', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('custom_map_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Seattle', max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('state', self.gf('django_localflavor_us.models.USStateField')(default='WA', max_length=2)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'stepping_out', ['Venue'])

        # Adding field 'Lesson.venue'
        db.add_column(u'stepping_out_lesson', 'venue',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Dance.venue'
        db.add_column(u'stepping_out_dance', 'venue',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'DanceTemplate.venue'
        db.add_column(u'stepping_out_dancetemplate', 'venue',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'LessonTemplate.venue'
        db.add_column(u'stepping_out_lessontemplate', 'venue',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'stepping_out.dance': {
            'Meta': {'ordering': "('start', 'end')", 'object_name': 'Dance'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'djs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'dj_for'", 'blank': 'True', 'through': u"orm['stepping_out.DanceDJ']", 'to': u"orm['stepping_out.Person']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'host_for'", 'blank': 'True', 'to': u"orm['stepping_out.Person']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'live_acts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stepping_out.LiveAct']", 'symmetrical': 'False', 'through': u"orm['stepping_out.DanceLiveAct']", 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'scheduled_dance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dances'", 'null': 'True', 'to': u"orm['stepping_out.ScheduledDance']"}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'stepping_out.dancedj': {
            'Meta': {'ordering': "('order', 'start', 'end')", 'object_name': 'DanceDJ'},
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Dance']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Person']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.danceliveact': {
            'Meta': {'ordering': "('order', 'start', 'end')", 'object_name': 'DanceLiveAct'},
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Dance']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live_act': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.LiveAct']"}),
            'order': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.dancetemplate': {
            'Meta': {'object_name': 'DanceTemplate'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'stepping_out.lesson': {
            'Meta': {'ordering': "('start', 'end')", 'object_name': 'Lesson'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lessons'", 'to': u"orm['stepping_out.Dance']"}),
            'dance_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stepping_out.Person']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'stepping_out.lessontemplate': {
            'Meta': {'object_name': 'LessonTemplate'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dance_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'dance_template': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lesson_templates'", 'null': 'True', 'to': u"orm['stepping_out.DanceTemplate']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Location']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'start_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.liveact': {
            'Meta': {'object_name': 'LiveAct'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'stepping_out.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Seattle'", 'max_length': '100'}),
            'custom_map_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'custom_map_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django_localflavor_us.models.USStateField', [], {'default': "'WA'", 'max_length': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'stepping_out.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.scheduleddance': {
            'Meta': {'object_name': 'ScheduledDance'},
            'banner': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'dance_template': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.DanceTemplate']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'weeks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "'1,2,3,4,5'", 'max_length': '9'})
        }
    }

    complete_apps = ['stepping_out']