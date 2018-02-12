from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch


from .voicelabel import VoiceLabel, Language, VoiceFragment
from .vs_element import VoiceServiceElement

class VoiceService(models.Model):
    _urls_name = 'service-development:voice-service'

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    creation_date = models.DateTimeField('date created', auto_now_add = True)
    modification_date = models.DateTimeField('date last modified', auto_now = True)
    active = models.BooleanField('Voice service active',
            help_text = "This voice service is only accessible for users when marked active.")
    _start_element = models.ForeignKey(
            VoiceServiceElement,
            related_name='%(app_label)s_%(class)s_related',
            null = True,
            blank = True)
    registration_choices = [('required', 'required (service does not function without Caller ID!)'),
                            ('preferred', 'preferred'),
                            ('disabled', 'disabled')]
    registration = models.CharField('User registration',max_length = 15, blank = False, choices = registration_choices)
    registration_language = models.BooleanField('Register Language preference', help_text= "The preferred language will be asked and stored during the user registration process", default = True)
    registration_name = models.BooleanField('Register spoken name', help_text = "The user will be asked to speak their name as part of the user registration process", default = False)

    supported_languages = models.ManyToManyField(Language, blank = True)

    @property
    def start_element(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceElement.objects.get_subclass(id = self._start_element.id)

    @property
    def supports_single_language(self):
        """
        Returns True if this service supports only a single language
        """
        return len(self.supported_languages.all()) == 1

    @property
    def registration_required(self):
        "Returns True if user registration is required"
        return self.registration == 'required'

    @property
    def registration_preferred_or_required(self):
        "Returns True if user registration is preferred or required"
        return (self.registration == 'preferred' or self.registration == 'required')

    @property
    def registration_disabled(self):
        "Returns True if user registration is disabled"
        return self.registration == 'disabled'
    
    def get_vxml_url(self):
        try:
            return reverse(self._urls_name, kwargs ={'voice_service_id': self.id})
        except NoReverseMatch:
            return "unknown"
    get_vxml_url.short_description = "VoiceXML endpoint URL"
    vxml_url = property(get_vxml_url)
    
    def __str__(self):
        return 'Voice Service: %s' % self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        if not self._start_element:
            errors.append('No starting element')
        else:
            associated_elements = self.voiceservicesubelement_set.all()
            for sub_element in associated_elements:
                errors.extend(sub_element.get_subclass_object().validator())
        if len(self.supported_languages.all()) == 0:
            errors.append('No supported languages')

        #deduplicate errors
        errors = list(set(errors))
        return errors

