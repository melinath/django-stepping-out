from django import forms

from stepping_out.models import ScheduledDance


class ScheduledDanceForm(forms.ModelForm):
    weeks = forms.MultipleChoiceField(choices=ScheduledDance.WEEK_CHOICES,
                                      widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ScheduledDance

    def __init__(self, *args, **kwargs):
        super(ScheduledDanceForm, self).__init__(*args, **kwargs)
        self.initial['weeks'] = self.instance.weeks.split(',')

    def clean_weeks(self):
        return ','.join(self.cleaned_data['weeks'])
