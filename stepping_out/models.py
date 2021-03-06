import datetime
import operator

from dateutil import rrule
from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import get_current_timezone, utc, make_aware
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import USStateField


class Location(models.Model):
    name = models.CharField(max_length=100)
    banner = models.ImageField(upload_to="stepping_out/location/banner/%Y/%m/%d",
                               blank=True)
    website = models.URLField(blank=True)
    #: URL for a custom map (for hard-to-find locations.)
    custom_map_url = models.URLField(blank=True,
                                     help_text="The long form of the link to "
                                               "a custom google map.")
    custom_map_image = models.ImageField(
        blank=True,
        upload_to="stepping_out/location/map/%Y/%m/%d"
    )
    neighborhood = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=100, default='Seattle')
    state = USStateField(default='WA')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_location_detail', (),
                {'slug': slugify(self.name), 'pk': self.pk})


class Person(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    user = models.OneToOneField('auth.User', blank=True, null=True)
    image = models.ImageField(upload_to='stepping_out/person/%Y/%m/%d',
                              blank=True)

    class Meta:
        verbose_name_plural = u'people'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_person_detail', (),
                {'slug': slugify(self.name), 'pk': self.pk})

    def get_recent_activity(self):
        """
        Returns a list of the times this person has filled any role
        at a dance in the last 60 days. Each item in the list is a tuple
        of (dance, roles). The list is ordered by time.

        """
        activity = {}
        now = datetime.datetime.now(utc)
        start = now - datetime.timedelta(days=60)
        dance_qs = Dance.objects.filter(start__gt=start, end__lt=now)
        for dance in dance_qs.filter(hosts=self):
            activity.setdefault(dance, []).append('hosted')

        for dance in dance_qs.filter(djs=self):
            activity.setdefault(dance, []).append('DJed at')

        for lesson in Lesson.objects.filter(dance__in=dance_qs, teachers=self):
            activity.setdefault(dance, []).append('taught {0} for'.format(lesson.name))

        activity = list(activity.iteritems())
        activity.sort(key=lambda item: item[0].end)
        activity.sort(key=lambda item: item[0].start)

        return activity

    def get_recent_activity_stats(self):
        """
        Returns a dictionary of counts for the number of times this
        person filled various roles in the last 60 days.

        """
        stats = {}
        now = datetime.datetime.now(utc)
        start = now - datetime.timedelta(days=60)
        dance_qs = Dance.objects.filter(start__gt=start, end__lt=now)
        stats['hosted'] = dance_qs.filter(hosts=self).count()
        stats['djed'] = dance_qs.filter(djs=self).count()
        stats['taught'] = Lesson.objects.filter(dance__in=dance_qs, teachers=self).count()
        return stats


class LiveAct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='stepping_out/live_act/%Y/%m/%d',
                              blank=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_liveact_detail', (),
                {'slug': slugify(self.name), 'pk': self.pk})


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
        ordering = ('order', 'start', 'end',)


class DanceDJ(BaseTimeOrderModel):
    person = models.ForeignKey(Person)
    dance = models.ForeignKey('Dance')

    @property
    def name(self):
        return self.person.name

    @property
    def image(self):
        return self.person.image

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_person_detail', (),
                {'pk': self.person_id})


class DanceLiveAct(BaseTimeOrderModel):
    live_act = models.ForeignKey(LiveAct)
    dance = models.ForeignKey('Dance')

    @property
    def name(self):
        return self.live_act.name

    @property
    def image(self):
        return self.live_act.image

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_liveact_detail', (),
                {'pk': self.live_act_id})


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
    tagline = models.CharField(max_length=100, blank=True)
    banner = models.ImageField(upload_to="stepping_out/dance/banner/%Y/%m/%d",
                               blank=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    hosts = models.ManyToManyField(Person, blank=True, related_name='host_for')
    djs = models.ManyToManyField(Person,
                                 through=DanceDJ,
                                 blank=True,
                                 related_name='dj_for')
    live_acts = models.ManyToManyField(LiveAct,
                                       through=DanceLiveAct,
                                       blank=True)
    venue = models.ForeignKey('Venue',
                              blank=True,
                              null=True,
                              related_name='dances')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    is_canceled = models.BooleanField(default=False)
    sites = models.ManyToManyField(Site, blank=True)

    # This field is used internally for recurring events to track when
    # a single instance is modified.
    original_day = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('start', 'end')

    def __unicode__(self):
        if self.start is None:
            return self.name
        start = self.start.astimezone(get_current_timezone())
        return u"{0} ({1})".format(self.name, start.strftime("%Y-%m-%d"))

    @models.permalink
    def get_absolute_url(self):
        tzinfo = get_current_timezone()
        start = self.start.astimezone(tzinfo)
        return ('stepping_out_dance_detail', (),
                {'slug': slugify(self.name),
                 'pk': self.pk,
                 'day': str(start.day).zfill(2),
                 'month': str(start.month).zfill(2),
                 'year': str(start.year).zfill(4)})


class Lesson(BasePriceModel):
    """
    A specific lesson.

    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    teachers = models.ManyToManyField(Person, blank=True)
    dance = models.ForeignKey(Dance, related_name='lessons', blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)
    series = models.ForeignKey('Series', related_name='lessons', blank=True, null=True)
    sites = models.ManyToManyField(Site, blank=True)

    # This field is used internally for recurring events to track when
    # a single instance is modified.
    original_day = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ('start', 'end')

    def __unicode__(self):
        if self.start is None:
            return self.name
        start = self.start.astimezone(get_current_timezone())
        if self.dance:
            return u"{0} ({1}, {2})".format(self.name, self.dance.name,
                                            start.strftime("%Y-%m-%d"))
        return u"{0} ({1})".format(self.name, start.strftime("%Y-%m-%d"))


class DanceTemplate(BasePriceModel):
    name = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=100, blank=True)
    banner = models.ImageField(
        upload_to="stepping_out/dance/banner/%Y/%m/%d",
        blank=True)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    sites = models.ManyToManyField(Site, blank=True)

    def __unicode__(self):
        return self.name

    def get_or_create_dance(self, start_day, venue=None):
        tzinfo = get_current_timezone()
        start = make_aware(datetime.datetime.combine(start_day, self.start_time),
                           tzinfo)
        end = make_aware(datetime.datetime.combine(start_day, self.end_time),
                         tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
            'banner': self.banner,
            'description': self.description,
            'location': self.location,
            'price': self.price,
            'student_price': self.student_price,
            'custom_price': self.custom_price,
            'start': start,
            'end': end,
            'original_day': start_day
        }
        if venue is not None:
            kwargs = {
                'original_day__year': start_day.year,
                'original_day__month': start_day.month,
                'original_day__day': start_day.day,
                'venue': venue,
            }
            dance, created = Dance.objects.get_or_create(defaults=defaults,
                                                         **kwargs)
        else:
            created = True
            dance = Dance.objects.create(**defaults)
        if created:
            dance.sites = self.sites.all()
            for lesson_template in self.lesson_templates.all():
                lesson_template.get_or_create_lesson(start_day, dance)
        return dance, created


class LessonTemplate(BasePriceModel):
    """
    A lesson which will be created at the same time that a dance is created.
    """
    dance_template = models.ForeignKey(DanceTemplate,
                                       related_name='lesson_templates',
                                       blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)
    sites = models.ManyToManyField(Site, blank=True)

    def __unicode__(self):
        if self.dance_template:
            return u"{0} ({1})".format(self.name, self.dance_template.name)
        return self.name

    def get_or_create_lesson(self, start_day, dance=None, series=None):
        """
        Gets or creates a lesson for the given Dance object and/or Series.

        """
        tzinfo = get_current_timezone()
        start = make_aware(datetime.datetime.combine(start_day, self.start_time),
                           tzinfo)
        end = make_aware(datetime.datetime.combine(start_day, self.end_time),
                         tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'price': self.price,
            'student_price': self.student_price,
            'custom_price': self.custom_price,
            'start': start,
            'end': end,
            'dance_included': self.dance_included,
            'dance': dance,
            'original_day': start_day,
        }
        if series is not None:
            kwargs = {
                'original_day__year': start_day.year,
                'original_day__month': start_day.month,
                'original_day__day': start_day.day,
            }
            lesson, created = Lesson.objects.get_or_create(defaults=defaults,
                                                           **kwargs)
        else:
            created = True
            lesson = Lesson.objects.create(**defaults)
        if created:
            lesson.sites = self.sites.all()
        return dance, created


class ScheduleBase(models.Model):
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
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    weeks = models.CommaSeparatedIntegerField(max_length=len(WEEKLY),
                                              default=WEEKLY)
    start_day = models.DateField(blank=True, null=True)
    end_day = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_weeks(self):
        return [week[1] for week in self.WEEK_CHOICES
                if unicode(week[0]) in self.weeks]

    def days_in_range(self, start_day, end_day):
        if end_day < start_day:
            start_day, end_day = end_day, start_day
        kwargs = {
            'byweekday': self.weekday,
            'dtstart': datetime.datetime.combine(start_day, datetime.time(0)),
            'until': datetime.datetime.combine(end_day, datetime.time(0)),
        }
        days = rrule.rrule(rrule.WEEKLY, **kwargs)

        return [day.date() for day in days
                if str(day.day // 7 + 1) in self.weeks]

    def _get_scheduled(self, start_day, end_day):
        raise NotImplementedError

    def _create_for_day(self, day):
        raise NotImplementedError

    def get_or_create_scheduled(self, start_day, end_day):
        all_days = self.days_in_range(start_day, end_day)
        scheduled = list(self._get_scheduled(start_day, end_day))
        scheduled_days = [s.original_day for s in scheduled]
        missing_days = set(all_days) - set(scheduled_days)
        for day in missing_days:
            scheduled.append(self._create_for_day(day))
        scheduled.sort(key=operator.attrgetter('original_day'))
        return scheduled


class Venue(ScheduleBase):
    """
    Model for a regularly-occuring dance venue.

    """
    name = models.CharField(max_length=100)
    banner = models.ImageField(
        upload_to="stepping_out/venue/banner/%Y/%m/%d",
        blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    dance_template = models.ForeignKey(DanceTemplate, blank=True, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_venue_detail', (),
                {'pk': self.pk, 'slug': slugify(self.name)})

    def __unicode__(self):
        return self.name

    def _get_scheduled(self, start_day, end_day):
        return self.dances.filter(original_day__gte=start_day,
                                  original_day__lte=end_day)

    def _create_for_day(self, day):
        if self.dance_template is None:
            raise ValueError
        return self.dance_template.get_or_create_dance(day, venue=self)[0]


class Series(ScheduleBase):
    """
    Model for a recurring lesson series.

    """
    name = models.CharField(max_length=100)
    banner = models.ImageField(
        upload_to="stepping_out/venue/banner/%Y/%m/%d",
        blank=True)
    description = models.TextField(blank=True)
    lesson_template = models.ForeignKey(LessonTemplate, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Series'

    def __unicode__(self):
        return self.name

    def _create_for_day(self, day):
        if self.lesson_template is None:
            raise ValueError
        return self.lesson_template.get_or_create_lesson(day, series=self)[0]

    def _get_scheduled(self, start_day, end_day):
        return self.lessons.filter(original_day__gte=start_day,
                                   original_day__lte=end_day)
