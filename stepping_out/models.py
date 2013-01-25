from django.contrib.localflavor.us.models import USStateField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address1 = models.CharField(max_length=150)
    address2 = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, default='Seattle')
    state = USStateField(default='WA')


class Person(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField('auth.User', blank=True, null=True)
    image = models.ImageField(upload_to='stepping_out/person/%Y/%m/%d', blank=True)


class LiveAct(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='stepping_out/live_music/%Y/%m/%d', blank=True)


class BaseTimeOrderModel(models.Model):
    """
    Abstract base model for things that are ordered over the course of an event,
    which thus have a start/end and an order.

    """
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class DanceDJ(BaseTimeOrderModel):
    person = models.ForeignKey(Person)
    dance = models.ForeignKey('Dance')


class DanceLiveAct(BaseTimeOrderModel):
    live_music = models.ForeignKey(LiveAct)
    dance = models.ForeignKey('Dance')


class BaseTimePriceModel(models.Model):
    """
    Base model for start/end time fields and price/student price fields.

    """
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    price = models.PositiveSmallIntegerField(default=0)
    student_price = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class Dance(BaseTimePriceModel):
    """
    A specific dance event.

    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    hosts = models.ManyToManyField(Person, blank=True, related_name='host_for')
    djs = models.ManyToManyField(Person, through=DanceDJ, blank=True, related_name='dj_for')
    live_acts = models.ManyToManyField(LiveAct, through=DanceLiveAct, blank=True)
    scheduled_dance = models.ForeignKey('ScheduledDance', blank=True, null=True)


class Lesson(BaseTimePriceModel):
    """
    A specific lesson.

    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    teachers = models.ManyToManyField(Person, blank=True)
    scheduled_lesson = models.ForeignKey('ScheduledLesson', blank=True, null=True)


class ScheduledDance(BaseTimePriceModel):
    """
    Overarching model for a weekly or biweekly dance.

    """
    # These choices match up with the datetime.date(time).weekday() method.
    WEEKDAY_CHOICES = (
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    )
    WEEK_CHOICES = (
        (1, _('First')),
        (2, _('Second')),
        (3, _('Third')),
        (4, _('Fourth')),
        (5, _('Fifth')),
    )
    WEEKLY = '1,2,3,4,5'
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    weeks = models.CommaSeparatedIntegerField(max_length=len(WEEKLY), default=WEEKLY)

    def __unicode__(self):
        return self.name

    def get_weeks(self):
        return [week[1] for week in self.WEEK_CHOICES if unicode(week[0]) in self.weeks]


class ScheduledLesson(BaseTimePriceModel):
    """
    A lesson attached to a scheduled dance.

    """
    scheduled_dance = models.ForeignKey(ScheduledDance)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.scheduled_dance.name)
