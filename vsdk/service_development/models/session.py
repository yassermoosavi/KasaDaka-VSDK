from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class CallSession(models.Model):
    start = models.DateTimeField(auto_now_add = True)
    #TODO: make some kind of handler when the Asterisk connection is closed, to officially end the session.
    end = models.DateTimeField(auto_now = True)
