from __future__ import print_function
from googleapiclient.discovery import build

from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow, Credentials
from oauth2client.file import Storage

from django.conf import settings


class CalendarException(Exception):
    pass


def add_calendar_event(request, event):

    flags = tools.argparser.parse_args([])

    storage = Storage('static/calendar.dat')
    FLOW = OAuth2WebServerFlow(
        client_id=settings.MEETUP_CLIENT_ID,
        client_secret=settings.MEETUP_CLIENT_SECRET,
        scope='https://www.googleapis.com/auth/calendar',
        user_agent=settings.MEETUP_CLIENT_NAME,
    )

    credentials = request.session.get('calendar_auth', None)
    if not credentials:
        credentials = tools.run_flow(FLOW, storage, flags)
    else:
        credentials = Credentials.new_from_json(credentials)

    service = build('calendar', 'v3', credentials=credentials)

    # Add event to the calendar
    event = service.events().insert(calendarId='primary', body=event).execute()
    if request.user.email != event['creator']['email']:
        service.events().delete(
            calendarId='primary', eventId=event['id']).execute()
        raise CalendarException(
            "Meetup registration email does not match the calendar email!")
    request.session['calendar_auth'] = credentials.to_json()
    print('Event created: %s' % (event.get('htmlLink')))
