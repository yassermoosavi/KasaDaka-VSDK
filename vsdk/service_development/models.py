from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import voicelabels

# Create your models here.
class VoiceServiceElement(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(
            max_length = 500,
            blank = True)

    def __str__(self):
        return "Element: %s" % self.name

class MessagePresentation(VoiceServiceElement):
    message = models.ForeignKey(
            voicelabels.models.VoiceLabel, 
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )
    final_element = models.BooleanField('This element will terminate the call',default = False)
    next_element = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related')

    def __str__(self):
        return 'Message Element: %s' % self.name

class Choice(VoiceServiceElement):
    question = models.ForeignKey(
            voicelabels.models.VoiceLabel, 
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            )

    def __str__(self):
        return self.name

class ChoiceOption(VoiceServiceElement): 
    parent = models.ForeignKey(
            Choice, 
            #controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
            related_name='%(app_label)s_%(class)s_parent_related')
    audio = models.ForeignKey(
            voicelabels.models.VoiceLabel, 
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            ) 
    redirect = models.ForeignKey(
            VoiceServiceElement, 
            #controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
            related_name='%(app_label)s_%(class)s_redirect_related')

    def __str__(self):
        return "(%s): %s" % (self.parent.name,self.name)

class DataPresentation(VoiceServiceElement):
    pass

class VoiceService(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10)
    creation_date = models.DateTimeField('date created', default=timezone.now)
    modification_date = models.DateTimeField('date last modified', default=timezone.now)
    active = models.BooleanField('Activate this voice service')
    start_element = models.ForeignKey(
            VoiceServiceElement,
            related_name='%(app_label)s_%(class)s_related')

    def __str__(self):
        return 'Voice Service: %s' % self.name

    def updateModificationDate(self):
        #misschien moet hier iets met pre_save? https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.pre_init
        self.modification_date = timezone.now()
        return


