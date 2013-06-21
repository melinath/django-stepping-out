from djam.riffs.models import ModelRiff

from stepping_out.models import ScheduledLesson, Lesson


class ScheduledLessonRiff(ModelRiff):
    model = ScheduledLesson


class LessonRiff(ModelRiff):
    model = Lesson


riffs = [ScheduledLessonRiff, LessonRiff]
