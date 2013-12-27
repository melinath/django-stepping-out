from djam.riffs.models import ModelRiff

from stepping_out.models import Lesson


class LessonRiff(ModelRiff):
    model = Lesson


riffs = [LessonRiff]
