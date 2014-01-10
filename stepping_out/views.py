import datetime
import itertools
import operator

from django.contrib.sites.models import Site
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.utils.timezone import get_current_timezone, now
from django.views.generic import DetailView, ListView, DateDetailView

from stepping_out.models import Venue, Dance, Location, Lesson, Series


def _get_or_create_scheduled(start, end, location=None, venues=None,
                             series=None):
        tzinfo = get_current_timezone()
        start_day = start.astimezone(tzinfo).date()
        end_day = end.astimezone(tzinfo).date()

        site = Site.objects.get_current()
        q = Q(original_day__gte=start_day,
              original_day__lte=end_day,
              sites=site,
              original_day__isnull=False)
        if location is not None:
            q = q & Q(location=location)
        dances = Dance.objects.filter(q).select_related('venue')
        lessons = Lesson.objects.filter(q).select_related('series')

        q = (Q(start_day__lte=start_day, end_day__gte=end_day) |
             Q(start_day__isnull=True, end_day__gte=end_day) |
             Q(start_day__lte=start_day, end_day__isnull=True) |
             Q(start_day__isnull=True, end_day__isnull=True))
        if venues is None and series is None:
            venues = Venue.objects.filter(q, dance_template__sites=site
                                          ).distinct()
            series = Series.objects.filter(q, lesson_template__sites=site
                                           ).distinct()

        scheduled_map = {}
        for s in itertools.chain(dances, lessons):
            if hasattr(s, 'venue'):
                scheduler = s.venue
            else:
                scheduler = s.series

            if scheduler is not None:
                scheduled_map.setdefault(s.original_day, set()).add(scheduler)

        for scheduler in itertools.chain(venues or [], series or []):
            for day in scheduler.days_in_range(start_day, end_day):
                if (day not in scheduled_map or
                        scheduler not in scheduled_map[day]):
                    scheduler._create_for_day(day)

        # Now we have to get the ones that actually fall in the time range.
        q = Q(end__gte=start,
              start__lte=end,
              start__isnull=False,
              sites=site)
        if location is not None:
            q = q & Q(location=location)
        dances = Dance.objects.filter(q).prefetch_related('lessons')
        lessons = Lesson.objects.filter(q)
        if venues:
            dances = dances.filter(venue__in=venues)
            lessons = []
        elif series:
            lessons = lessons.filter(series__in=series)
            dances = []

        return sorted(itertools.chain(dances, lessons),
                      key=operator.attrgetter('start'))


def _group_events(events):
    tzinfo = get_current_timezone()
    events_grouped = SortedDict()
    for event in events:
        start_date = event.start.astimezone(tzinfo).date()
        events_grouped.setdefault(start_date, []).append(event)
    return events_grouped


class EventListView(ListView):
    context_object_name = 'events'
    template_name = 'stepping_out/event/list.html'

    def get_range(self):
        raise NotImplementedError

    def get_queryset(self):
        start, end = self.get_range()
        return _get_or_create_scheduled(start, end)

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        today = now().astimezone(get_current_timezone()).date()
        events_grouped = _group_events(context['events'])
        context.update({
            'events_grouped': events_grouped.items(),
            'today': today
        })
        return context


class UpcomingEventView(EventListView):
    def get_range(self):
        start = now() + datetime.timedelta(hours=.5)
        return start, start + datetime.timedelta(7)


class FakeSlugDetailMixin(object):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        expected_url = self.object.get_absolute_url()
        if request.path_info != expected_url:
            return HttpResponseRedirect(expected_url)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class FakeSlugDetailView(FakeSlugDetailMixin, DetailView):
    pass


class DanceDetailView(FakeSlugDetailMixin, DateDetailView):
    context_object_name = 'dance'
    template_name = 'stepping_out/dance/detail.html'
    date_field = 'start'
    allow_future = True

    def get_queryset(self):
        site = Site.objects.get_current()
        return Dance.objects.select_related('venue'
                                            ).filter(sites=site)


class LocationDetailView(FakeSlugDetailView):
    model = Location
    context_object_name = 'venue'

    def get_context_data(self, **kwargs):
        context = super(LocationDetailView, self).get_context_data(**kwargs)

        start = now() + datetime.timedelta(hours=.5)
        end = start + datetime.timedelta(7)

        events = _get_or_create_scheduled(start, end,
                                          location=self.object)
        events_grouped = _group_events(events)

        today = now().astimezone(get_current_timezone()).date()
        context.update({
            'events_grouped': events_grouped.items(),
            'today': today,
        })
        return context


class VenueDetailView(FakeSlugDetailMixin, DetailView):
    model = Venue
    context_object_name = 'venue'

    def get_queryset(self):
        qs = super(VenueDetailView, self).get_queryset()
        return qs.filter(sites=Site.objects.get_current())

    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)

        start = now() + datetime.timedelta(hours=.5)
        end = start + datetime.timedelta(7)

        events = _get_or_create_scheduled(start, end,
                                          venues=[self.object])
        events_grouped = _group_events(events)

        today = now().astimezone(get_current_timezone()).date()
        context.update({
            'events_grouped': events_grouped.items(),
            'today': today,
        })
        return context
