# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Venue'
        db.create_table(u'stepping_out_venue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('custom_map', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('city', self.gf('django.db.models.fields.CharField')(default='Seattle', max_length=100)),
            ('state', self.gf('django_localflavor_us.models.USStateField')(default='WA', max_length=2)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'stepping_out', ['Venue'])

        # Adding model 'Person'
        db.create_table(u'stepping_out_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'stepping_out', ['Person'])

        # Adding model 'LiveAct'
        db.create_table(u'stepping_out_liveact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'stepping_out', ['LiveAct'])

        # Adding model 'DanceDJ'
        db.create_table(u'stepping_out_dancedj', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Person'])),
            ('dance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Dance'])),
        ))
        db.send_create_signal(u'stepping_out', ['DanceDJ'])

        # Adding model 'DanceLiveAct'
        db.create_table(u'stepping_out_danceliveact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('live_act', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.LiveAct'])),
            ('dance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Dance'])),
        ))
        db.send_create_signal(u'stepping_out', ['DanceLiveAct'])

        # Adding model 'Dance'
        db.create_table(u'stepping_out_dance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('student_price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('custom_price', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True)),
            ('scheduled_dance', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dances', null=True, to=orm['stepping_out.ScheduledDance'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'stepping_out', ['Dance'])

        # Adding M2M table for field hosts on 'Dance'
        m2m_table_name = db.shorten_name(u'stepping_out_dance_hosts')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dance', models.ForeignKey(orm[u'stepping_out.dance'], null=False)),
            ('person', models.ForeignKey(orm[u'stepping_out.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['dance_id', 'person_id'])

        # Adding model 'Lesson'
        db.create_table(u'stepping_out_lesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('student_price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('custom_price', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True)),
            ('dance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lessons', to=orm['stepping_out.Dance'])),
            ('scheduled_lesson', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lessons', null=True, to=orm['stepping_out.ScheduledLesson'])),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dance_included', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'stepping_out', ['Lesson'])

        # Adding unique constraint on 'Lesson', fields ['slug', 'dance']
        db.create_unique(u'stepping_out_lesson', ['slug', 'dance_id'])

        # Adding M2M table for field teachers on 'Lesson'
        m2m_table_name = db.shorten_name(u'stepping_out_lesson_teachers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lesson', models.ForeignKey(orm[u'stepping_out.lesson'], null=False)),
            ('person', models.ForeignKey(orm[u'stepping_out.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['lesson_id', 'person_id'])

        # Adding model 'ScheduledDance'
        db.create_table(u'stepping_out_scheduleddance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('student_price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('custom_price', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='scheduled_dances', null=True, to=orm['stepping_out.Venue'])),
            ('weekday', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('weeks', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default='1,2,3,4,5', max_length=9)),
            ('start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'stepping_out', ['ScheduledDance'])

        # Adding model 'ScheduledLesson'
        db.create_table(u'stepping_out_scheduledlesson', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
            ('student_price', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('custom_price', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('scheduled_dance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scheduled_lessons', to=orm['stepping_out.ScheduledDance'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('venue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stepping_out.Venue'], null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('dance_included', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'stepping_out', ['ScheduledLesson'])

        # Adding unique constraint on 'ScheduledLesson', fields ['slug', 'scheduled_dance']
        db.create_unique(u'stepping_out_scheduledlesson', ['slug', 'scheduled_dance_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'ScheduledLesson', fields ['slug', 'scheduled_dance']
        db.delete_unique(u'stepping_out_scheduledlesson', ['slug', 'scheduled_dance_id'])

        # Removing unique constraint on 'Lesson', fields ['slug', 'dance']
        db.delete_unique(u'stepping_out_lesson', ['slug', 'dance_id'])

        # Deleting model 'Venue'
        db.delete_table(u'stepping_out_venue')

        # Deleting model 'Person'
        db.delete_table(u'stepping_out_person')

        # Deleting model 'LiveAct'
        db.delete_table(u'stepping_out_liveact')

        # Deleting model 'DanceDJ'
        db.delete_table(u'stepping_out_dancedj')

        # Deleting model 'DanceLiveAct'
        db.delete_table(u'stepping_out_danceliveact')

        # Deleting model 'Dance'
        db.delete_table(u'stepping_out_dance')

        # Removing M2M table for field hosts on 'Dance'
        db.delete_table(db.shorten_name(u'stepping_out_dance_hosts'))

        # Deleting model 'Lesson'
        db.delete_table(u'stepping_out_lesson')

        # Removing M2M table for field teachers on 'Lesson'
        db.delete_table(db.shorten_name(u'stepping_out_lesson_teachers'))

        # Deleting model 'ScheduledDance'
        db.delete_table(u'stepping_out_scheduleddance')

        # Deleting model 'ScheduledLesson'
        db.delete_table(u'stepping_out_scheduledlesson')


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
        u'stepping_out.dance': {
            'Meta': {'ordering': "('start', 'end')", 'object_name': 'Dance'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'djs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'dj_for'", 'blank': 'True', 'through': u"orm['stepping_out.DanceDJ']", 'to': u"orm['stepping_out.Person']"}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'host_for'", 'blank': 'True', 'to': u"orm['stepping_out.Person']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'live_acts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stepping_out.LiveAct']", 'symmetrical': 'False', 'through': u"orm['stepping_out.DanceLiveAct']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'scheduled_dance': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dances'", 'null': 'True', 'to': u"orm['stepping_out.ScheduledDance']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        u'stepping_out.lesson': {
            'Meta': {'ordering': "('start', 'end')", 'unique_together': "(('slug', 'dance'),)", 'object_name': 'Lesson'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lessons'", 'to': u"orm['stepping_out.Dance']"}),
            'dance_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'scheduled_lesson': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lessons'", 'null': 'True', 'to': u"orm['stepping_out.ScheduledLesson']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['stepping_out.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.liveact': {
            'Meta': {'object_name': 'LiveAct'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'stepping_out.person': {
            'Meta': {'object_name': 'Person'},
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.scheduleddance': {
            'Meta': {'object_name': 'ScheduledDance'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'scheduled_dances'", 'null': 'True', 'to': u"orm['stepping_out.Venue']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'weeks': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': "'1,2,3,4,5'", 'max_length': '9'})
        },
        u'stepping_out.scheduledlesson': {
            'Meta': {'unique_together': "(('slug', 'scheduled_dance'),)", 'object_name': 'ScheduledLesson'},
            'custom_price': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'dance_included': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'scheduled_dance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'scheduled_lessons'", 'to': u"orm['stepping_out.ScheduledDance']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100'}),
            'start': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'student_price': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'venue': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['stepping_out.Venue']", 'null': 'True', 'blank': 'True'})
        },
        u'stepping_out.venue': {
            'Meta': {'object_name': 'Venue'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Seattle'", 'max_length': '100'}),
            'custom_map': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'}),
            'state': ('django_localflavor_us.models.USStateField', [], {'default': "'WA'", 'max_length': '2'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['stepping_out']