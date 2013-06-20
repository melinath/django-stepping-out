from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView, DateDetailView

from stepping_out.models import ScheduledDance, Venue, Person, LiveAct, Dance
from stepping_out.views import ScheduledDanceDetailView, UpcomingDancesView


urlpatterns = patterns('',
    url(r'^$',
        UpcomingDancesView.as_view(),
        name='stepping_out_dances'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\w-]+)/$',
        DateDetailView.as_view(queryset=Dance.objects.select_related('venue', 'scheduled_dance'),
                               template_name='stepping_out/dance/detail.html',
                               date_field='start',
                               allow_future=True,
                               month_format='%m'),
        name='stepping_out_dance_detail'),

    url(r'^scheduled-dances/$',
        ListView.as_view(queryset=ScheduledDance.objects.order_by('name'),
                         template_name='stepping_out/scheduleddance/list.html',
                         context_object_name='scheduled_dances'),
        name='stepping_out_scheduled_dances'),
    url(r'^scheduled-dances/(?P<slug>[\w-]+)/$',
        ScheduledDanceDetailView.as_view(template_name='stepping_out/scheduleddance/detail.html'),
        name='stepping_out_scheduled_dance_detail'),

    url(r'^venues/$',
        ListView.as_view(queryset=Venue.objects.order_by('name'),
                         template_name='stepping_out/venues.html',
                         context_object_name='venues'),
        name='stepping_out_venues'),
    url(r'^venues/(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=Venue,
                           context_object_name='venue'),
        name='stepping_out_venue_detail'),

    url(r'^people/(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=Person,
                           context_object_name='person'),
        name='stepping_out_person_detail'),
    url(r'^live_acts/(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=LiveAct,
                           context_object_name='live_act'),
        name='stepping_out_liveact_detail'),
)
