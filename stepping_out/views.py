import datetime

from django.http import HttpResponseRedirect
from django.utils.datastructures import SortedDict
from django.utils.timezone import get_current_timezone, utc, now
from django.views.generic import DetailView, ListView, DateDetailView

from stepping_out.models import ScheduledDance, Dance


class UpcomingDancesView(ListView):
    model = Dance
    context_object_name = 'dances'
    template_name = 'stepping_out/dance/list.html'

    def get_queryset(self):
        for sd in ScheduledDance.objects.all():
            sd.get_or_create_next_dance()

        # Return dances that end more than half an hour from now or start less
        # than a week from now.
        start = datetime.datetime.now(get_current_timezone()).astimezone(utc)
        end = start + datetime.timedelta(7)
        start = start + datetime.timedelta(hours=.5)
        return Dance.objects.filter(end__gt=start, start__lt=end, is_canceled=False
                           ).select_related('venue', 'scheduled_dance',
                                            'dancedj_set', 'dancedj_set__person'
                           ).prefetch_related('lessons', 'lessons__teachers',
                                              'hosts', 'live_acts')

    def get_context_data(self, **kwargs):
        context = super(UpcomingDancesView, self).get_context_data(**kwargs)
        tzinfo = get_current_timezone()
        today = now().astimezone(tzinfo).date()
        dances_grouped = SortedDict()
        for dance in context['dances']:
            start_date = dance.start.astimezone(tzinfo).date()
            dances_grouped.setdefault(start_date, []).append(dance)
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
    queryset = Dance.objects.select_related('venue')
    template_name = 'stepping_out/dance/detail.html'
    date_field = 'start'
    allow_future = True


class ScheduledDanceDetailView(FakeSlugDetailMixin, DetailView):
    model = ScheduledDance
    context_object_name = 'scheduled_dance'

    def get_context_data(self, **kwargs):
        context = super(ScheduledDanceDetailView, self).get_context_data(**kwargs)
        context['next_dance'] = self.object.get_or_create_next_dance()[0]
        return context
