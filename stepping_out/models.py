import datetime

from django.contrib.sites.models import Site
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.timezone import get_current_timezone, utc, make_aware
from django.utils.translation import ugettext_lazy as _
from django_localflavor_us.models import USStateField


class Venue(models.Model):
    name = models.CharField(max_length=100)
    banner = models.ImageField(upload_to="stepping_out/venue/banner/%Y/%m/%d",
                               blank=True)
    website = models.URLField(blank=True)
    #: URL for a custom map (for hard-to-find venues.)
    custom_map_url = models.URLField(blank=True,
                                     help_text="The long form of the link to "
                                               "a custom google map.")
    custom_map_image = models.ImageField(
        blank=True,
        upload_to="stepping_out/venue/map/%Y/%m/%d"
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
        return ('stepping_out_venue_detail', (),
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
    is_canceled = models.BooleanField(default=False)
    sites = models.ManyToManyField(Site, blank=True)

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
    venue = models.ForeignKey(Venue, blank=True, null=True)
    teachers = models.ManyToManyField(Person, blank=True)
    dance = models.ForeignKey(Dance, related_name='lessons')
    scheduled_lesson = models.ForeignKey('ScheduledLesson',
                                         blank=True,
                                         null=True,
                                         related_name='lessons')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)

    class Meta:
        ordering = ('start', 'end')

    def __unicode__(self):
        if self.start is None:
            return self.name
        start = self.start.astimezone(get_current_timezone())
        return u"{0} ({1}, {2})".format(self.name, self.dance.name,
                                        start.strftime("%Y-%m-%d"))


class ScheduledDance(BasePriceModel):
    """
    Overarching model for a regularly-occuring dance venue.

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
    banner = models.ImageField(
        upload_to="stepping_out/scheduled_dance/banner/%Y/%m/%d",
        blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    weeks = models.CommaSeparatedIntegerField(max_length=len(WEEKLY),
                                              default=WEEKLY)

    # Deprecated/elsewhere.
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    venue = models.ForeignKey(Venue,
                              blank=True,
                              null=True,
                              related_name='scheduled_dances')
    sites = models.ManyToManyField(Site, blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ('stepping_out_scheduled_dance_detail', (),
                {'pk': self.pk, 'slug': slugify(self.name)})

    def __unicode__(self):
        return self.name

    def get_weeks(self):
        return [week[1] for week in self.WEEK_CHOICES
                if unicode(week[0]) in self.weeks]

    def days_in_month(self, month):
        # month is an integer, 1-12.
        days = []
        now = datetime.datetime.now(get_current_timezone())
        month_start = datetime.date(now.year, month, 1)
        until_first = (7 - month_start.weekday() + self.weekday) % 7

        first_day = month_start + datetime.timedelta(until_first)

        for week in self.WEEK_CHOICES:
            if unicode(week[0]) in self.weeks:
                days.append(first_day + datetime.timedelta(7 * (week[0] - 1)))

        return days

    def get_next_date(self):
        now = datetime.datetime.now(get_current_timezone())
        today = now.date()
        time = now.time()

        for month in [now.month, now.month + 1]:
            days = self.days_in_month(month)
            for day in days:
                if day > today:
                    return day
                if day == today and self.start > time:
                    return day

        raise ValueError("No next date found.")

    def get_or_create_dance(self, start_day):
        tzinfo = get_current_timezone()
        start = make_aware(datetime.datetime.combine(start_day, self.start),
                           tzinfo)
        end = make_aware(datetime.datetime.combine(start_day, self.end),
                         tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
            'banner': self.banner,
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
            dance.sites = self.sites.all()
            for scheduled_lesson in self.scheduled_lessons.all():
                scheduled_lesson.get_or_create_lesson(dance)
        return dance, created

    def get_or_create_next_dance(self):
        return self.get_or_create_dance(self.get_next_date())


class ScheduledLesson(BasePriceModel):
    """
    A lesson attached to a scheduled dance.

    """
    scheduled_dance = models.ForeignKey(ScheduledDance,
                                        related_name='scheduled_lessons')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    start = models.TimeField(blank=True, null=True)
    end = models.TimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)

    def get_or_create_lesson(self, dance):
        """
        Gets or creates a lesson for the given dance.

        :raises: ValueError if the dance's scheduled dance is not the same
                 as the lesson's scheduled dance.

        """
        if dance.scheduled_dance_id != self.scheduled_dance_id:
            raise ValueError
        tzinfo = get_current_timezone()
        start_day = dance.start.astimezone(tzinfo).date()
        start = make_aware(datetime.datetime.combine(start_day, self.start),
                           tzinfo)
        end = make_aware(datetime.datetime.combine(start_day, self.end),
                         tzinfo)
        if end < start:
            # Then it ends the next day.
            end = end + datetime.timedelta(1)

        defaults = {
            'name': self.name,
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

    def __unicode__(self):
        return u"{0} ({1})".format(self.name, self.scheduled_dance.name)


class DanceTemplate(BasePriceModel):
    name = models.CharField(max_length=100, blank=True)
    tagline = models.CharField(max_length=100, blank=True)
    banner = models.ImageField(
        upload_to="stepping_out/scheduled_dance/banner/%Y/%m/%d",
        blank=True)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    sites = models.ManyToManyField(Site, blank=True)


class LessonTemplate(BasePriceModel):
    """
    A lesson which will be created at the same time that a dance is created.
    """
    dance_template = models.ForeignKey(DanceTemplate,
                                       related_name='lesson_templates')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    venue = models.ForeignKey(Venue, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    dance_included = models.BooleanField(default=True)
