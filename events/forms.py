from django import forms
from events.models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'name', 'description', 'visibility',
            'start_time', 'address', 'latitude', 'longitude', 'organizer'
        )
        widgets = {
            'address': forms.TextInput(attrs={'size': 80}),
            'organizer': forms.HiddenInput()
        }
