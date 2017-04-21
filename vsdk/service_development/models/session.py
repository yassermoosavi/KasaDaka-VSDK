from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from . import KasaDakaUser
from . import VoiceService, VoiceServiceElement
from . import Language

class CallSession(models.Model):
    start = models.DateTimeField(auto_now_add = True)
    #TODO: make some kind of handler when the Asterisk connection is closed, to officially end the session.
    end = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(KasaDakaUser, on_delete = models.PROTECT, null = True, blank = True)
    service = models.ForeignKey(VoiceService, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return "%s (%s)" % (str(self.user), str(self.start))

    def get_language(self):
        if self.user:
            return self.user.language 
        #TODO maybe return default language?
        return None
    
    def record_step(self, element):
        step = CallSessionStep(session = self, _visited_element = element)
        step.save()
        return

    def link_to_user(self, user):
        self.user = user
        self.save()
        return self

class CallSessionStep(models.Model):
    time = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete = models.PROTECT, related_name = "steps")
    _visited_element = models.ForeignKey(VoiceServiceElement, on_delete = models.SET_NULL, null = True)

    def __str__(self):
        return "%s: %s -> %s" % (str(self.session), str(self.time), str(self.visited_element))

    @property
    def visited_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._visited_element.id)


def lookup_or_create_session(voice_service, session_id=None):
    if session_id:
        session = get_object_or_404(CallSession, pk = session_id)
    else:
        session = CallSession(service = voice_service) 
        session.save()
    return session
