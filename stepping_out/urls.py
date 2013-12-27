from django.conf.urls import patterns, url
from django.views.generic import ListView

from stepping_out.models import ScheduledDance, Location, Person, LiveAct
from stepping_out.views import (ScheduledDanceDetailView, UpcomingDancesView,
                                FakeSlugDetailView, DanceDetailView,
                                LocationDetailView)


urlpatterns = patterns('',
    url(r'^$',
        UpcomingDancesView.as_view(),
        name='stepping_out_dances'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<pk>\d+)/(?:(?P<slug>[\w-]+)/)?$',
        DanceDetailView.as_view(month_format='%m'),
        name='stepping_out_dance_detail'),

    url(r'^scheduled-dances/$',
        ListView.as_view(queryset=ScheduledDance.objects.order_by('name'),
                         template_name='stepping_out/scheduleddance/list.html',
                         context_object_name='scheduled_dances'),
        name='stepping_out_scheduled_dances'),
    url(r'^scheduled-dances/(?P<pk>\d+)/(?:(?P<slug>[\w-]+)/)?$',
        ScheduledDanceDetailView.as_view(template_name='stepping_out/scheduleddance/detail.html'),
        name='stepping_out_scheduled_dance_detail'),

    url(r'^locations/$',
        ListView.as_view(queryset=Location.objects.order_by('name'),
                         template_name='stepping_out/locations.html',
                         context_object_name='locations'),
        name='stepping_out_locations'),
    url(r'^locations/(?P<pk>\d+)/(?:(?P<slug>[\w-]+)/)?$',
        LocationDetailView.as_view(),
        name='stepping_out_location_detail'),

    url(r'^people/(?P<pk>\d+)/(?:(?P<slug>[\w-]+)/)?$',
        FakeSlugDetailView.as_view(model=Person,
                                   context_object_name='person'),
        name='stepping_out_person_detail'),
    url(r'^live_acts/(?P<pk>\d+)/(?:(?P<slug>[\w-]+)/)?$',
        FakeSlugDetailView.as_view(model=LiveAct,
                                   context_object_name='live_act'),
        name='stepping_out_liveact_detail'),
)
