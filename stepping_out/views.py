from django.views.generic import DetailView

from stepping_out.models import ScheduledDance


class ScheduledDanceDetailView(DetailView):
    model = ScheduledDance
    context_object_name = 'scheduled_dance'

    def get_context_data(self, **kwargs):
        context = super(ScheduledDanceDetailView, self).get_context_data(**kwargs)
        context['next_dance'] = self.object.get_or_create_next_dance()[0]
        return context
