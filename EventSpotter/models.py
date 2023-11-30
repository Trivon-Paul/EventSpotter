from django.db import models
from django.db.models import Model


class EventsSaved(models.Model):
    user = models.CharField(max_length=60)
    event_name = models.CharField(max_length=60)
    event_url = models.URLField(max_length=200)
    image_url = models.URLField(max_length=200)
    event_date = models.CharField(max_length=60)
    event_time = models.CharField(max_length=20)
    event_venue = models.CharField(max_length=60)
    event_address = models.CharField(max_length=60)
    event_state = models.CharField(max_length=60)
    event_city = models.CharField(max_length=60)


class Search(models.Model):
    keyword = models.CharField(max_length=60)
    location = models.CharField(max_length=60)
