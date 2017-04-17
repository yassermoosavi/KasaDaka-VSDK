from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from voicelabels.models import Language
from . import VoiceService

class KasaDakaUser(models.Model):
    """
    User that belongs to a Voice Service on this system
    """
    #TODO: disallow deletion of users?
    callerID = models.CharField('phone number',max_length=100, unique = True)
    first_name = models.CharField('first name', max_length = 100, blank = True)
    last_name = models.CharField('last name', max_length=100, blank = True)
    creation_date = models.DateTimeField(auto_now_add = True)
    modification_date = models.DateTimeField(auto_now = True)
    #TODO maybe also delete user if language is deleted? 
    language = models.ForeignKey(Language,on_delete = models.PROTECT, null = True)
    service = models.ForeignKey(VoiceService, on_delete = models.CASCADE, null= True)

    def __str__(self):
        if not (self.first_name or self.last_name):
            return "%s" % self.callerID
        else:
            return "%s %s (%s)" % (self.first_name, self.last_name, self.callerID)


