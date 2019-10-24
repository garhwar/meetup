from django.db import models
from django.contrib.auth.models import User

# Create your models here.


EVENT_TYPE = (
    (1, 'PUBLIC'),
    (2, 'PRIVATE')
)


class Event(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=3600)  # seconds
    description = models.TextField(max_length=1000)
    visibility = models.IntegerField(choices=EVENT_TYPE, default=1)
    address = models.CharField(max_length=500)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    organizer = models.ForeignKey(
        User, related_name='organized_events', on_delete=models.CASCADE)
    members = models.ManyToManyField(User, related_name='participated_events')
