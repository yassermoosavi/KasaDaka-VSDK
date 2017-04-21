import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from vsdk.usage.models.session import lookup_or_create_session, CallSession

class TestCallSession:
    
    def test_init(self):
        obj = mixer.blend('usage.CallSession')
        assert obj.pk == 1

    def test_str(self):
        obj = mixer.blend('usage.CallSession')
        assert str(obj) == str(obj.user) + " (" + str(obj.start) + ")"

    def test_get_language(self):
        user = mixer.blend('usage.KasaDakaUser')
        obj = mixer.blend('usage.CallSession',
                user = user)
        assert obj.get_language() == obj.user.language , 'Language should be language of user'

        obj = mixer.blend('usage.CallSession',
                user = None)
        assert obj.get_language() == None , 'Session without user (and thus language) is possible'

    def test_record_step(self):
        session = mixer.blend('usage.CallSession')
        choice_element = mixer.blend('service_development.Choice')
        session.record_step(choice_element)
        assert session.steps.all()[0].visited_element == choice_element

        
        session = mixer.blend('usage.CallSession')
        choice_elements = mixer.cycle(11).blend('service_development.Choice')
        message_elements = mixer.cycle(10).blend('service_development.MessagePresentation')
        general_element = mixer.blend('service_development.VoiceServiceElement')
        session.record_step(message_elements[0])

        for element in choice_elements:
            session.record_step(element)
            session.record_step(general_element)
        
        step_visted_elements = []
        for step in session.steps.all():
            step_visted_elements.append(step.visited_element)
        for element in choice_elements:
            assert element in step_visted_elements

        assert message_elements[0] in step_visted_elements
        assert general_element in step_visted_elements
        
        count = 0
        for element in step_visted_elements:
            if element == general_element:
                count += 1
        assert count == 11
        assert session.steps.all()[5].session == session

    def test_link_to_user(self):
        session = mixer.blend('usage.CallSession',
                user=None)
        assert session.user == None
        user = mixer.blend('usage.KasaDakaUser')
        session.link_to_user(user)
        assert session.user == user

class TestCallSessionStep:

    def test_init(self):
        obj = mixer.blend('usage.CallSessionStep')
        assert obj.pk == 1

    def test_str(self):
        obj = mixer.blend('usage.CallSessionStep')
        assert str(obj) == str(obj.session) + ": " + str(obj.time) + " -> " + str(obj.visited_element)

def test_lookup_or_create_session():
        session = mixer.blend('usage.CallSession')
        assert lookup_or_create_session(None, session.id)== session
        assert isinstance(lookup_or_create_session(None,None), CallSession)
        vs = mixer.blend('service_development.VoiceService')
        assert lookup_or_create_session(vs, None).service == vs

    


