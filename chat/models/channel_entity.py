from django.db import models
from django.contrib.auth.models import User


class ChannelEntity(models.Model):
    channel_name = models.CharField(max_length=50, blank=False)
    users = models.ManyToManyField(User)
