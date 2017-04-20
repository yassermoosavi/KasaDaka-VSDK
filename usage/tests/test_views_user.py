from xml.etree import ElementTree as ET
from django.test.utils import setup_test_environment
from django.test import Client, TestCase
from django.urls import reverse

from ..views import user
from ..models import KasaDakaUser, CallSession, CallSessionStep
from service_development.models import VoiceService
from voicelabels.models import Language, VoiceLabel


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
                requires_registration= True,

                )
        
        self.voice_service.supported_languages.add(self.language)
        CallSession.objects.create(service = self.voice_service)
        
        self.session = CallSession.objects.all()[0]
        self.caller_id = "123"


        


    def test_user_registration_invalid_request(self):
        #empty request should raise error
        self.assertRaises(ValueError, self.client.get, self.user_registration_form_url)

    def test_user_registration_get_request(self):

        response = self.client.get(self.user_registration_form_url,
                {'caller_id' : self.caller_id,
                    'session_id' : self.session.id})
        assert response.status_code == 200
        print(response.content)
        assert response.content == ""
        assert ET.fromstring(response.content), 'Should produce valid XML'

        #TODO
        #assert response.context == ""

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


