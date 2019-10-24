from django.conf.urls import url
from events import views

from django.contrib.auth.decorators import login_required

app_name = 'events'

urlpatterns = [
    url(r'^events/$', views.EventListView.as_view(), name='browse'),
    url(
        r'^event/create/$',
        login_required(views.EventCreateView.as_view()),
        name='event-create'
    ),
    url(
        r'^event/(?P<pk>\d+)/$',
        login_required(views.EventDetailView.as_view()),
        name='event-detail'
    ),
    url(
        r'^event/(?P<pk>\d+)/join/$',
        login_required(views.EventJoinView.as_view()),
        name='event-join'
    ),
]
