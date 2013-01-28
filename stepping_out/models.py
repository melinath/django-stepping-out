import datetime

from django.contrib.localflavor.us.models import USStateField
from django.db import models
from django.utils.timezone import get_current_timezone, utc
from django.utils.translation import ugettext_lazy as _


class Venue(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    website = models.URLField(blank=True)
    #: URL for a custom map (for hard-to-find venues.)
    custom_map = models.URLField(blank=True,
                                 help_text="The long form of the link to a "
                                           "custom google map.")
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100, default='Seattle')
    state = USStateField(default='WA')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    user = models.OneToOneField('auth.User', blank=True, null=True)
    image = models.ImageField(upload_to='stepping_out/person/%Y/%m/%d',
                              blank=True)

    class Meta:
        verbose_name_plural = u'people'

    def __unicode__(self):
        return self.name


class LiveAct(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='stepping_out/live_music/%Y/%m/%d',
                              blank=True)

    def __unicode__(self):
        return self.name


class BaseTimeOrderModel(models.Model):
    """
    Abstract base model for things that are ordered over the course of an
    event, which thus have a start/end and an order.

    """
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        abstract = True


class DanceDJ(BaseTimeOrderModel):
    person = models.ForeignKey(Person)
    dance = models.ForeignKey('Dance')


class DanceLiveAct(BaseTimeOrderModel):
    live_music = models.ForeignKey(LiveAct)
    dance = models.ForeignKey('Dance')


class BasePriceModel(models.Model):
    """
    Base model for start/end time fields and price/student price fields.

    """
    price = models.PositiveSmallIntegerField(default=0)
    student_price = models.PositiveSmallIntegerField(blank=True, null=True)
    #: In case some other type of pricing is called for.
    custom_price = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True


class Dance(BasePriceModel):
    """
    A specific dance event.

    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    hosts = models.ManyToManyField(Person, blank=True, related_name='host_for')
    djs = models.ManyToManyField(Person,
                                 through=DanceDJ,
                                 blank=True,
                                 related_name='dj_for')
    live_acts = models.ManyToManyField(LiveAct,
                                       through=DanceLiveAct,
                                       blank=True)
    scheduled_dance = models.ForeignKey('ScheduledDance',
                                        blank=True,
                                        null=True,
                                        related_name='dances')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class Lesson(BasePriceModel):
    """
    A specific lesson.

    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    teachers = models.ManyToManyField(Person, blank=True)
    dance = models.ForeignKey(Dance)
    scheduled_lesson = models.ForeignKey('ScheduledLesson',
                                         blank=True,
                                         null=True,
                                         related_name='lessons')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)

    class Meta:
        unique_together = ('slug', 'dance')

    def __unicode__(self):
        return self.name


class ScheduledDance(BasePriceModel):
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
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    venue = models.ForeignKey(Venue,
                              blank=True,
                              null=True,
                              related_name='scheduled_dances')
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    weeks = models.CommaSeparatedIntegerField(max_length=len(WEEKLY),
                                              default=WEEKLY)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_weeks(self):
        return [week[1] for week in self.WEEK_CHOICES
                if unicode(week[0]) in self.weeks]

    def get_or_create_next_dance(self):
        today = datetime.date.today()
        days = (7 - today.weekday() + self.weekday) % 7
        start_day = today + datetime.timedelta(days)
        tzinfo = get_current_timezone()
        start = datetime.datetime.combine(start_day, self.start
                                ).replace(tzinfo=tzinfo)
        end = datetime.datetime.combine(start_day, self.end
                              ).replace(tzinfo=tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'venue': self.venue,
            'price': self.price,
            'student_price': self.student_price,
            'custom_price': self.custom_price,
            'start': start,
            'end': end,
        }
        utc_start = start.astimezone(utc)
        kwargs = {
            'start__year': utc_start.year,
            'start__month': utc_start.month,
            'start__day': utc_start.day,
            'scheduled_dance': self
        }
        dance, created = Dance.objects.get_or_create(defaults=defaults,
                                                     **kwargs)
        if created:
            for scheduled_lesson in self.scheduled_lessons.all():
                scheduled_lesson.get_or_create_next_lesson(dance)
        return dance, created


class ScheduledLesson(BasePriceModel):
    """
    A lesson attached to a scheduled dance.

    """
    scheduled_dance = models.ForeignKey(ScheduledDance,
                                        related_name='scheduled_lessons')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)

    def get_or_create_next_lesson(self, dance):
        if dance.scheduled_dance != self.scheduled_dance:
            raise ValueError
        scheduled_dance = self.scheduled_dance
        today = datetime.date.today()
        days = (7 - today.weekday() + scheduled_dance.weekday) % 7
        start_day = today + datetime.timedelta(days)
        tzinfo = get_current_timezone()
        start = datetime.datetime.combine(start_day, self.start
                                ).replace(tzinfo=tzinfo)
        end = datetime.datetime.combine(start_day, self.end
                              ).replace(tzinfo=tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'venue': self.venue,
            'price': self.price,
            'student_price': self.student_price,
            'custom_price': self.custom_price,
            'start': start,
            'end': end,
            'dance_included': self.dance_included,
            'dance': dance
        }
        utc_start = start.astimezone(utc)
        kwargs = {
            'start__year': utc_start.year,
            'start__month': utc_start.month,
            'start__day': utc_start.day,
            'scheduled_lesson': self
        }
        return Lesson.objects.get_or_create(defaults=defaults,
                                            **kwargs)

    class Meta:
        unique_together = ('slug', 'scheduled_dance')

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.scheduled_dance.name)
