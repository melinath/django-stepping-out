from daguerre.widgets import AreaWidget
from django.contrib import admin
from django.db import models
from django.template.loader import render_to_string

from stepping_out.forms import (VenueForm, LocationForm, DanceCreateForm,
                                LessonTemplateForm)
from stepping_out.models import (Venue,
                                 Location, Dance, Lesson, Person, DanceDJ,
                                 DanceLiveAct, DanceTemplate, LessonTemplate)


class VenueAdmin(admin.ModelAdmin):
    form = VenueForm
    fieldsets = (
        (None, {
            'fields': ('name', 'banner', 'description', 'website'),
        }),
        ('Scheduling', {
            'fields': ('weekday', 'weeks', 'start_day', 'end_day',
                       'dance_template'),
        }),
    )
    list_display = ['name', 'get_schedule']
    list_filter = ['weekday']

    def get_schedule(self, obj):
        return render_to_string('stepping_out/scheduleddance/_schedule.html',
                                {'scheduled_dance': obj})
    get_schedule.short_description = 'Schedule'


class LessonTemplateInline(admin.StackedInline):
    model = LessonTemplate
    form = LessonTemplateForm
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Scheduling', {
            'fields': ('location', 'start_time', 'end_time', 'dance_template'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price',
                       'dance_included')
        })
    )
    extra = 1

    def save_model(self, request, obj, form, change):
        super(LessonTemplateInline, self).save_model(request, obj, form, change)
        obj.sites = obj.dance_template.sites.all()


class DanceTemplateAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'tagline', 'banner', 'description', 'sites'),
        }),
        ('Scheduling', {
            'fields': ('location', 'start_time', 'end_time'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price')
        })
    )
    inlines = [LessonTemplateInline]
    list_display = ['name', 'location', 'start_time'] #, 'get_schedule']
    list_filter = ['location',]

    def get_schedule(self, obj):
        return render_to_string('stepping_out/scheduleddance/_schedule.html',
                                {'scheduled_dance': obj})
    get_schedule.short_description = 'Schedule'


class LocationAdmin(admin.ModelAdmin):
    form = LocationForm
    list_display = ['name', 'address', 'city', 'state']
    list_filter = ['state']


class LessonInline(admin.StackedInline):
    model = Lesson
    fieldsets = (
        (None, {
            'fields': ('name', 'description'),
        }),
        ('Scheduling', {
            'fields': ('location', 'start', 'end', 'dance',
                       'teachers'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price',
                       'dance_included')
        })
    )
    extra = 1
    filter_horizontal = ('teachers',)


class DanceDJInline(admin.TabularInline):
    model = DanceDJ
    extra = 1
    sortable_field_name = "order"


class DanceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'tagline', 'banner', 'description',
                       'venue', 'sites'),
        }),
        ('Scheduling', {
            'fields': ('is_canceled', 'location', 'start', 'end', 'hosts'),
        }),
        ('Pricing', {
            'fields': ('price', 'student_price', 'custom_price')
        })
    )
    inlines = [LessonInline, DanceDJInline]
    filter_horizontal = ('hosts',)
    list_display = ['name', 'start', 'location', 'venue']
    list_filter = ['is_canceled', 'location', 'venue']
    date_hierarchy = 'start'
    ordering = ('-start',)
    list_per_page = 20

    # Won't actually be used by ModelAdmin, but riff will catch.
    add_form = DanceCreateForm
    add_fieldsets = (
        (None, {
            'fields': ('venue', 'template', 'start_day'),
        }),
    )


class PersonAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ImageField: {'widget': AreaWidget},
    }
    list_display = ['name']
    ordering = ('name',)


admin.site.register(Venue, VenueAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Dance, DanceAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(DanceTemplate, DanceTemplateAdmin)
