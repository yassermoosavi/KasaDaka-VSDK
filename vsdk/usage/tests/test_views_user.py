from xml.etree import ElementTree as ET

import mock

from django.test.utils import setup_test_environment
from django.test import Client, TestCase
from django.urls import reverse
from django.core.files import File
from django.core.files.storage import Storage

from ..views import user
from ..models import KasaDakaUser, CallSession, CallSessionStep
from vsdk.service_development.models import VoiceService
from vsdk.voicelabels.models import Language, VoiceLabel, VoiceFragment


class TestUserRegistration(TestCase):
#    setup_test_environment()
    client = Client()
    user_registration_form_url =reverse('service-development:usage:user-registration') 


    def setUp(self):
        self.voice_label = VoiceLabel.objects.create(
                name = "test voicelabel")

        self.language = Language.objects.create(
                name="Nederlands",
                code="nl",
                voice_label =  self.voice_label,
                error_message = self.voice_label)

        self.voice_service = VoiceService.objects.create(
                name="testservice",
                description="bla",
                active = True,
                requires_registration= True)
        self.voice_service.supported_languages.add(self.language)

        self.audio_file = mock.MagicMock(spec=File, name='audio')
        self.audio_file.name = 'audio.wav'

        # Mock storage to emulate having a file in the FileField
        self.storage_mock = mock.MagicMock(spec=Storage, name='StorageMock')
        self.storage_mock.url = mock.MagicMock(name='url')
        self.storage_mock.url.return_value = '/static/audio.wav'

        with mock.patch('django.core.files.storage.default_storage._wrapped', self.storage_mock):
            self.voice_fragment = VoiceFragment.objects.create(
                    parent = self.voice_label,
                    language = self.language,
                    audio = self.audio_file)
        
        self.session = CallSession.objects.create(service = self.voice_service)
        self.caller_id = "123"

    def test_user_registration_invalid_request(self):
        #empty request should raise error
        self.assertRaises(ValueError, self.client.get, self.user_registration_form_url)

    def test_user_registration_get_request(self):

        response = self.client.get(self.user_registration_form_url,
                {'caller_id' : self.caller_id,
                    'session_id' : self.session.id})
        assert response.status_code == 200
        #TODO
        #assert response.context == ""
        
        
        assert ET.fromstring(response.content), 'Should produce valid XML'



    def test_user_registration_post_request(self):
        response = self.client.post(
                self.user_registration_form_url,
                {
                    'caller_id': self.caller_id,
                    'session_id': self.session.id,
                    'language_id': self.language.id}
                )

        #user should be created and redirected
        assert response.status_code == 302

        #check if user exists
        assert KasaDakaUser.objects.get(caller_id = self.caller_id, service = self.voice_service).service == self.voice_service


