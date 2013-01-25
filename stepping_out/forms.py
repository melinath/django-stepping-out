from django import forms
from django.core.exceptions import ValidationError
from pygeocoder import Geocoder

from stepping_out.models import ScheduledDance, Venue


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


class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        exclude = ('latitude', 'longitude')

    def clean(self):
        cleaned_data = super(VenueForm, self).clean()
        self._result = None
        components = [cleaned_data.get(k)
                      for k in ('address', 'city', 'state')]
        if all(components):
            address = " ".join(components)
            result = Geocoder.geocode(address)
            if not result.valid_address:
                raise ValidationError("{0} is not a valid address.".format(
                                      cleaned_data['address']))
            if result.count > 1:
                raise ValidationError("{0} locations found for {1}".format(
                                      result.count,
                                      cleaned_data['address']))

            self._result = result
            cleaned_data['address'] = "{0} {1}".format(result.street_number,
                                                       result.route)
        return cleaned_data

    def _post_clean(self):
        super(VenueForm, self)._post_clean()
        if self._result:
            instance = self.instance
            coordinates = self._result.coordinates
            instance.latitude, instance.longitude = coordinates
