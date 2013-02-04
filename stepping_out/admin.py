from django.core.urlresolvers import reverse
from django.contrib import admin, messages
from django.http import HttpResponseRedirect

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
    actions = ['create_next_dances']

    def create_next_dances(self, request, queryset):
        for scheduled_dance in queryset:
            dance, created = scheduled_dance.get_or_create_next_dance()
            url = reverse('admin:stepping_out_dance_change', args=(dance.pk,))
            if created:
                message = u"Created {0}".format(dance)
                level = messages.success
            else:
                message = u"{0} already exists".format(dance)
                level = messages.info
            if len(queryset) > 1:
                message = u"{0}: {1}".format(message, url)
            level(request, message)
        if len(queryset) == 1:
            return HttpResponseRedirect(url)


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
