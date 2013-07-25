import datetime

from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.utils.timezone import get_current_timezone, utc, now
from django.views.generic import DetailView, ListView, DateDetailView

from stepping_out.models import ScheduledDance, Dance, Venue


def _get_upcoming_dances(scheduled_dances):
    for sd in scheduled_dances:
        sd.get_or_create_next_dance()

    # Return dances that end more than half an hour from now or start less
    # than a week from now.
    start = now().astimezone(utc)
    end = start + datetime.timedelta(7)
    start = start + datetime.timedelta(hours=.5)
    return Dance.objects.filter(end__gt=start,
                                start__lt=end,
                                sites=Site.objects.get_current(),
                                ).prefetch_related('lessons')


def _group_dances(dances):
    tzinfo = get_current_timezone()
    dances_grouped = SortedDict()
    for dance in dances:
        start_date = dance.start.astimezone(tzinfo).date()
        dances_grouped.setdefault(start_date, []).append(dance)
    return dances_grouped


class UpcomingDancesView(ListView):
    model = Dance
    context_object_name = 'dances'
    template_name = 'stepping_out/dance/list.html'

    def get_queryset(self):
        site = Site.objects.get_current()
        scheduled = ScheduledDance.objects.filter(sites=site)
        return _get_upcoming_dances(scheduled)

    def get_context_data(self, **kwargs):
        context = super(UpcomingDancesView, self).get_context_data(**kwargs)
        today = now().astimezone(get_current_timezone()).date()
        dances_grouped = _group_dances(context['dances'])
        context.update({
            'dances_grouped': dances_grouped.items(),
            'today': today
        })
        return context


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
        return Dance.objects.select_related('venue', 'scheduled_dance'
                                            ).filter(sites=site)


class VenueDetailView(FakeSlugDetailView):
    model = Venue
    context_object_name = 'venue'

    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)

        dances = _get_upcoming_dances(self.object.scheduled_dances.all())
        dances = dances.filter(venue=self.object)
        dances_grouped = _group_dances(dances)

        context.update({
            'dances_grouped': dances_grouped.items(),
            'today': now().astimezone(get_current_timezone()).date()
        })
        return context


class ScheduledDanceDetailView(FakeSlugDetailMixin, DetailView):
    model = ScheduledDance
    context_object_name = 'scheduled_dance'

    def get_queryset(self):
        qs = super(ScheduledDanceDetailView, self).get_queryset()
        return qs.filter(sites=Site.objects.get_current())

    def get_context_data(self, **kwargs):
        context = super(ScheduledDanceDetailView, self).get_context_data(**kwargs)

        dances = _get_upcoming_dances([self.object])
        dances = dances.filter(scheduled_dance=self.object)
        dances_grouped = _group_dances(dances)

        context.update({
            'dances_grouped': dances_grouped.items(),
            'today': now().astimezone(get_current_timezone()).date()
        })
        return context
