from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import voicelabels

# Create your models here.
class VoiceServiceElement(models.Model):
    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)
    name = models.CharField(max_length=100)
    service = models.ForeignKey('VoiceService', on_delete = models.CASCADE)
    description = models.CharField(
            max_length = 500,
            blank = True)
    voice_label = models.ForeignKey(
            voicelabels.models.VoiceLabel,
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

class MessagePresentation(VoiceServiceElement):
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


    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        #TODO: check all children (choice options)
        
        if self.voice_label:
            return self.voice_label.validator()
        else:
            return ['No VoiceLabel in element: "%s"'%self.name]

class ChoiceOption(VoiceServiceElement):
    parent = models.ForeignKey(
            Choice,
            #TODO: controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
            related_name='%(app_label)s_%(class)s_parent_related')
    redirect = models.ForeignKey(
            VoiceServiceElement, 
            #TODO: controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    def __str__(self):
        return "(%s): %s" % (self.parent.name,self.name)
    
    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        #check if voice label is present
        if self.voice_label:
            errors.extend(self.voice_label.validator())
        else:
            errors.append('No VoiceLabel in choice option: "%s"'%self.name)

        #check if redirect is present
        if not self.redirect:
            errors.append('No redirect in choice option: "%s"'%self.name)
        #check whether element that will be redirected to is appointed to the same voice service
        elif not self.redirect in self.service.get_elements():
            errors.append('Redirect "%s" in choice option "%s" does not belong to same voice service'% (self.redirect.name, self.name))

        return errors

 
class DataPresentation(VoiceServiceElement):
    pass

class VoiceService(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=10)
    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)
    active = models.BooleanField('Voice service active')
    start_element = models.ForeignKey(
            VoiceServiceElement,
            related_name='%(app_label)s_%(class)s_related',
            null = True,
            blank = True)

    supported_languages = models.ManyToManyField(voicelabels.models.Language, blank = True)

    def __str__(self):
        return 'Voice Service: %s' % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        if not self.start_element:
            errors.append('No starting element')
        else:
            errors.extend(self.start_element.validator())
        if len(self.supported_languages.all()) == 0:
            errors.append('No supported languages')
        return errors

    def get_elements(self):
        return []
