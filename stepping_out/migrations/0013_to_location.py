# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        Venue = orm['stepping_out.Venue']
        Location = orm['stepping_out.Location']

        for v in Venue.objects.all():
            l = Location.objects.create(
                name=v.name,
                banner=v.banner,
                website=v.website,
                custom_map_url=v.custom_map_url,
                custom_map_image=v.custom_map_image,
                neighborhood=v.neighborhood,
                address=v.address,
                city=v.city,
                state=v.state,
                latitude=v.latitude,
                longitude=v.longitude
            )
            v.lesson_set.update(location=l)
            v.lessontemplate_set.update(location=l)
            v.dance_set.update(location=l)
            v.dancetemplate_set.update(location=l)

    def backwards(self, orm):
        "Write your backwards methods here."
        Venue = orm['stepping_out.Venue']
        Location = orm['stepping_out.Location']

        for l in Location.objects.all():
            v = Location.objects.create(
                name=l.name,
                banner=l.banner,
                website=l.website,
                custom_map_url=l.custom_map_url,
                custom_map_image=l.custom_map_image,
                neighborhood=l.neighborhood,
                address=l.address,
                city=l.city,
                state=l.state,
                latitude=l.latitude,
                longitude=l.longitude
            )
            l.lesson_set.update(venue=v)
            l.lessontemplate_set.update(venue=v)
            l.dance_set.update(venue=v)
            l.dancetemplate_set.update(venue=v)

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
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
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
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
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
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stepping_out.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
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
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
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
        },
        u'stepping_out.venue': {
            'Meta': {'object_name': 'Venue'},
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
        }
    }

    complete_apps = ['stepping_out']
    symmetrical = True
