from django.contrib import admin

from stepping_out.forms import ScheduledDanceForm, VenueForm
from stepping_out.models import ScheduledLesson, ScheduledDance, Venue


class ScheduledLessonInline(admin.StackedInline):
    model = ScheduledLesson
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'scheduled_dance'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price')
        })
    )
    extra = 1


class ScheduledDanceAdmin(admin.ModelAdmin):
    model = ScheduledLesson
    form = ScheduledDanceForm
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'website'),
        }),
        ('Scheduling', {
            'fields': ('venue', 'start', 'end', 'weekday', 'weeks'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price')
        })
    )
    inlines = [ScheduledLessonInline]


class VenueAdmin(admin.ModelAdmin):
    model = Venue
    form = VenueForm


admin.site.register(ScheduledDance, ScheduledDanceAdmin)
admin.site.register(Venue, VenueAdmin)
