from djam.riffs.models import ModelRiff

from stepping_out.models import ScheduledLesson


class ScheduledLessonRiff(ModelRiff):
    model = ScheduledLesson


riffs = [ScheduledLessonRiff]
