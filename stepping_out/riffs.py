from djam.riffs.models import ModelRiff
from django.template.loader import render_to_string

from stepping_out.forms import (LessonCreateForm, LessonTemplateForm,
                                ScheduleBaseForm)
from stepping_out.models import Lesson, LessonTemplate, Series


class LessonRiff(ModelRiff):
    model = Lesson

    create_kwargs = {
        'form_class': LessonCreateForm,
        'fieldsets': (
            (None, {
                'fields': ('series', 'template', 'start_day'),
            }),
        )
    }

    update_kwargs = {
        'fieldsets': (
            (None, {
                'fields': ('name', 'description', 'series', 'sites'),
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
    }

    list_kwargs = {
        'order': ('-start',),
        'filters': ('location', 'series'),
        'columns': ('name', 'start', 'location', 'series'),
        'paginate_by': 20,
    }


class LessonTemplateRiff(ModelRiff):
    model = LessonTemplate

    create_kwargs = {
        'form_class': LessonTemplateForm,
        'fieldsets': (
            (None, {
                'fields': ('name', 'description', 'sites'),
            }),
            ('Scheduling', {
                'fields': ('location', 'start_time', 'end_time'),
            }),
            ('Pricing', {
                'fields': ('price', 'student_price', 'custom_price',
                           'dance_included')
            })
        )
    }
    update_kwargs = create_kwargs.copy()
    update_kwargs['fieldsets'][1][1]['fields'] += ('dance_template',)


def _get_schedule(obj):
    return render_to_string('stepping_out/scheduleddance/_schedule.html',
                            {'scheduled_dance': obj})
_get_schedule.short_description = 'Schedule'


class SeriesRiff(ModelRiff):
    model = Series

    create_kwargs = {
        'form_class': ScheduleBaseForm,
        'fieldsets': (
            (None, {
                'fields': ('name', 'banner', 'description'),
            }),
            ('Scheduling', {
                'fields': ('weekday', 'weeks', 'start_day', 'end_day',
                           'lesson_template'),
            }),
        )
    }
    update_kwargs = create_kwargs

    list_kwargs = {
        'filters': ('weekday',),
        'columns': ('name', _get_schedule),
    }


riffs = [LessonRiff, LessonTemplateRiff, SeriesRiff]
