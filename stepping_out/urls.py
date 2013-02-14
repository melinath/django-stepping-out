from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from stepping_out.models import ScheduledDance, Venue, Person, LiveAct
from stepping_out.views import ScheduledDanceDetailView, DanceListView


urlpatterns = patterns('',
    url(r'^$',
        DanceListView.as_view(),
        name='stepping_out_dances'),

    url(r'^scheduled-dances/$',
        ListView.as_view(queryset=ScheduledDance.objects.order_by('name'),
                         template_name='stepping_out/index.html',
                         context_object_name='scheduled_dances'),
        name='stepping_out_scheduled_dances'),
    url(r'^scheduled-dances/(?P<slug>[\w-]+)/$',
        ScheduledDanceDetailView.as_view(),
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
