from django.conf.urls import patterns, url
from django.views.generic import ListView

from stepping_out.models import ScheduledDance


urlpatterns = patterns('',
    url(r'^$', ListView.as_view(queryset=ScheduledDance.objects.order_by('name'),
                                template_name='stepping_out/index.html',
                                context_object_name='scheduled_dances')),
)
