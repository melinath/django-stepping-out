from djam.riffs.models import ModelRiff

from stepping_out.forms import LessonCreateForm
from stepping_out.models import Lesson


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


riffs = [LessonRiff]
