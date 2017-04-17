from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .user import KasaDakaUser
from .voiceservice import VoiceService, VoiceServiceElement
from voicelabels.models import Language

class CallSession(models.Model):
    start = models.DateTimeField(auto_now_add = True)
    #TODO: make some kind of handler when the Asterisk connection is closed, to officially end the session.
    end = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(KasaDakaUser, on_delete = models.PROTECT)
    service = models.ForeignKey(VoiceService, on_delete = models.SET_NULL, null= True)

    def __str__(self):
        return "%s (%s)" % (str(self.user), str(self.start))

    def get_language(self):
        return Language.objects.all()[0]
        #return self.user.language 

class CallSessionStep(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete = models.PROTECT, related_name = "steps")
    visited_element = models.ForeignKey(VoiceServiceElement, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return "%s: %s -> %s" % (str(self.session), str(self.time), str(self.visited_element))

