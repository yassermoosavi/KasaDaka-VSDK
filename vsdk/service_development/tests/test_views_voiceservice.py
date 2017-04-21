from xml.etree import ElementTree as ET

import mock
import random
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files import File
from django.core.files.storage import Storage

from ..models import KasaDakaUser, CallSession, CallSessionStep
from ..models import VoiceService, Choice, ChoiceOption
from ..models import Language, VoiceLabel, VoiceFragment

from .helpers import create_sample_voice_service

class TestVoiceServiceView(TestCase):
    client = Client()
    caller_id = "1234"

    def setUp(self):
        create_sample_voice_service(self)
        self.voice_service_urls_name = self.voice_service._urls_name 
        self.voice_service_url = reverse(self.voice_service_urls_name,
                kwargs = {'voice_service_id': self.voice_service.id})
        self.voice_service_url_plus_session = reverse(self.voice_service_urls_name,
                kwargs = {'voice_service_id': self.voice_service.id,
                    'session_id': self.session.id})

    def test_voice_service_start_without_session_known_callerid(self):
        """
        If the CallerID is provided which has a registered user, but not the session_id,
        a new session should be created and the user redirected to the starting element
        of the voice service.
        """
        self.voice_service.requires_registration = True
        self.voice_service.save()

        response = self.client.get(self.voice_service_url,
                {'callerid': self.caller_id})
        
        new_session_id = CallSession.objects.all().filter(user = self.user).order_by('-start')[0].id
        expected_redirection_url = reverse(self.voice_service.start_element._urls_name,
                kwargs = {'element_id': self.voice_service.start_element.id,
                    'session_id': new_session_id})
        self.assertRedirects(response,expected_redirection_url)

    def test_voice_service_start_without_session_unknown_callerid_registration_required(self):
        """
        If the CallerID that is provided is not known, and registration is required,
        user should be sent to registration form.
        """
        self.voice_service.requires_registration = True
        self.voice_service.save()
        caller_id =  random.randint(100000,999999)
        response = self.client.get(self.voice_service_url,
                {'callerid': caller_id})
        session_id = CallSession.objects.all().order_by('-start')[0].id

        self.assertRedirects(response,reverse('service-development:user-registration')+"?caller_id="+str(caller_id)+"&session_id="+str(session_id))



    def test_voice_service_start_without_session_unknown_callerid_registration_not_required(self):
        """
        If the CallerID that is provided is not registered as an user,
        and registration is NOT required,
        user should be sent to the language selection section.
        """
        self.voice_service.requires_registration = False
        self.voice_service.save()
        caller_id =  random.randint(100000,999999)
        response = self.client.get(self.voice_service_url,
                {'callerid': caller_id})
        session_id = CallSession.objects.all().order_by('-start')[0].id
        pass
        #TODO TODO
        #self.assertRedirects(response,reverse('service-development:user-registration'))

    def test_voice_service_start_without_session_without_callerid_registration_not_required(self):
        """
        When no callerid is provided, the user should only be redirected to the
        starting element of the voice service, when the voice service does
        not require registration.
        """
        self.voice_service.requires_registration = False
        self.voice_service.save()
        pass

    def test_voice_service_start_without_session_without_callerid_registration_required(self):
        """
        When no callerid is provided, the user should only be redirected to the
        starting element of the voice service, when the voice service does
        not require registration.
        """
        self.voice_service.requires_registration = True
        self.voice_service.save()
        pass

    def test_voice_service_start_with_session_id(self):
        pass

    
