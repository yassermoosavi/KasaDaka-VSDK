from django.db import models
from model_utils.managers import InheritanceManager
from django.urls import reverse

from .voicelabel import VoiceLabel

class VoiceServiceElement(models.Model):

    #use django_model_utils to be able to find out what is the subclass of this element
    #see: https://django-model-utils.readthedocs.io/en/latest/managers.html#inheritancemanager
    objects = InheritanceManager()

    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)
    name = models.CharField(max_length=100)
#    service = models.ForeignKey('VoiceService', on_delete = models.CASCADE)
    description = models.CharField(
            max_length = 500,
            blank = True)
    voice_label = models.ForeignKey(
            VoiceLabel,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    def __str__(self):
        return "Element: %s" % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        if self.voice_label:
            return self.voice_label.validator()
        else:
            return ['No VoiceLabel in element: "%s"'%self.name]

    def get_voice_fragment_url(self, language):
        return self.voice_label.get_voice_fragment_url(language)

    def get_absolute_url(self, session):
        #this is a dirty hack to refer to the subclass object of this reference, and then call the same method there.
        #return reverse('service_development:choice', args=[str(self.id),str(session.id)])
        #TODO what happens here? error message?
        #subclass_objects = self.select_subclasses()
        #if 
     #   return 
        #return VoiceServiceElement.objects.get_subclass(pk=self.id)
        return reverse(self._urls_name, kwargs= {'element_id':str(self.id), 'session_id':session.id})

