from django.contrib import admin

from stepping_out.forms import ScheduledDanceForm, VenueForm
from stepping_out.models import (ScheduledLesson, ScheduledDance,
                                 Venue, Dance, Lesson, Person)


class ScheduledLessonInline(admin.StackedInline):
    model = ScheduledLesson
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'scheduled_dance'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price',
                       'dance_included')
        })
    )
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


class ScheduledDanceAdmin(admin.ModelAdmin):
    form = ScheduledDanceForm
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'website'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'weekday', 'weeks'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price')
        })
    )
    inlines = [ScheduledLessonInline]
    prepopulated_fields = {"slug": ("name",)}


class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    prepopulated_fields = {"slug": ("name",)}


class LessonInline(admin.StackedInline):
    model = Lesson
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'dance',
                       'teachers'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price',
                       'dance_included')
        })
    )
    extra = 1
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('teachers',)


class DanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'scheduled_dance',
                       'hosts'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price')
        })
    )
    inlines = [LessonInline]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ('hosts',)


class PersonAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(ScheduledDance, ScheduledDanceAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Dance, DanceAdmin)
admin.site.register(Person, PersonAdmin)
