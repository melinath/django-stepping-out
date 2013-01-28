from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView

from stepping_out.models import ScheduledDance, Venue


urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=ScheduledDance.objects.order_by('name'),
                         template_name='stepping_out/index.html',
                         context_object_name='scheduled_dances'),
        name='stepping_out_index'),
    url(r'^(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=ScheduledDance,
                           context_object_name='scheduled_dance'),
        name='stepping_out_scheduled_dance_detail'),
    url(r'^venues/(?P<slug>[\w-]+)/$',
        DetailView.as_view(model=Venue,
                           context_object_name='venue'),
        name='stepping_out_venue_detail'),
)
