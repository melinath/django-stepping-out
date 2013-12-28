from django.core.exceptions import ValidationError
import floppyforms as forms
from pygeocoder import Geocoder

from stepping_out.models import (Venue, Location, Dance, DanceTemplate,
                                 Lesson, LessonTemplate)


class VenueForm(forms.ModelForm):
    weeks = forms.MultipleChoiceField(choices=Venue.WEEK_CHOICES,
                                      widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Venue

    def __init__(self, *args, **kwargs):
        super(VenueForm, self).__init__(*args, **kwargs)
        self.initial['weeks'] = self.instance.weeks.split(',')

    def clean_weeks(self):
        return ','.join(self.cleaned_data['weeks'])


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('latitude', 'longitude')

    def clean(self):
        cleaned_data = super(LocationForm, self).clean()
        fields = ('address', 'city', 'state')

        self._result = None
        components = [cleaned_data.get(f) for f in fields]
        # Only do geocode query if all components are clean and
        # at least one field has changed value.
        if all(components) and any(f in self.changed_data for f in fields):
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
        super(LocationForm, self)._post_clean()
        if self._result:
            instance = self.instance
            coordinates = self._result.coordinates
            instance.latitude, instance.longitude = coordinates


class DanceCreateForm(forms.ModelForm):
    start_day = forms.DateField()
    template = forms.ModelChoiceField(DanceTemplate.objects.all(),
                                      required=False)

    class Meta:
        model = Dance
        fields = ('venue',)

    def save(self, **kwargs):
        start_day = self.cleaned_data['start_day']
        template = self.cleaned_data['template']
        venue = self.instance.venue

        if not template and venue and venue.dance_template:
            template = venue.dance_template

        if template:
            return template.get_or_create_dance(start_day, venue)[0]

        return super(DanceCreateForm, self).save(**kwargs)


class LessonCreateForm(forms.ModelForm):
    start_day = forms.DateField()
    template = forms.ModelChoiceField(LessonTemplate.objects.all(),
                                      required=False)

    class Meta:
        model = Lesson
        fields = ('series',)

    def save(self, **kwargs):
        start_day = self.cleaned_data['start_day']
        template = self.cleaned_data['template']
        series = self.instance.series

        if not template and series and series.lesson_template:
            template = series.lesson_template

        if template:
            return template.get_or_create_dance(start_day, series)[0]

        return super(DanceCreateForm, self).save(**kwargs)
