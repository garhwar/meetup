from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from events.models import Event
from events.forms import EventForm

from .calendar import add_calendar_event
from datetime import timedelta


class EventListView(ListView):

    model = Event
    paginate_by = 12

    def get_queryset(self):
        return Event.objects.filter(visibility=1)


class EventDetailView(DetailView):

    model = Event


class EventCreateView(CreateView):

    model = Event
    form_class = EventForm
    success_url = "/meetup/events"

    def get_initial(self):
        initial = super().get_initial()
        initial['organizer'] = self.request.user
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['maps_api_key'] = settings.MAPS_API_KEY
        return context


class EventJoinView(View):

    def post(self, request, pk):
        user = request.user
        event_obj = get_object_or_404(Event, pk=pk)
        try:
            # Add event to user's calendar
            event = {
                'summary': event_obj.name,
                'location': event_obj.address,
                'description': event_obj.description,
                'start': {
                    'dateTime': event_obj.start_time.strftime(
                        "%Y-%m-%dT%H:%M:%S+05:30"),
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': (event_obj.start_time + timedelta(
                                 seconds=event_obj.duration
                                 )).strftime("%Y-%m-%dT%H:%M:%S+05:30"),
                    'timeZone': 'Asia/Kolkata',
                },
            }
            add_calendar_event(request, event)
        except Exception as e:
            return HttpResponse(e)
        else:
            event_obj.members.add(user)
        return HttpResponseRedirect(
            reverse('events:event-detail', kwargs={'pk': pk})
        )
