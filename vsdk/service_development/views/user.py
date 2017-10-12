from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import KasaDakaUser, CallSession

from ..models import Language

class KasaDakaUserRegistration(TemplateView):

    def user_registration_form(self, request, session, caller_id):
        """
        Renders the user registration VoiceXML form.
        This form consists of:
        - Selecting the preferred language
        """

        #get all supported languages
        languages = session.service.supported_languages.all()
        pass_on_variables = {'session_id':session.id,
                'caller_id':caller_id}
        context = {'languages':languages,
                'pass_on_variables': pass_on_variables,
                'redirect_url': reverse('service-development:user-registration'),
                }
        return render(request, 'user_registration.xml', context, content_type='text/xml')

    def post(self, request):
        """
        Registers the user to the system (POST), or provides the registration 'form' (GET).
        """
        #If POST and all required elements for user registration are filled
        if set(('caller_id','session_id','language_id')) <= set(request.POST):
            caller_id = request.POST['caller_id']
            session = get_object_or_404(CallSession, pk = request.POST['session_id'])
            language = get_object_or_404(Language, pk = request.POST['language_id'])

            #register the user and link the session to the user
            user = KasaDakaUser(caller_id = caller_id,
                    language = language,
                    service = session.service)
            user.save()
            session.link_to_user(user)

            #redirect back to start of voice service
            return redirect('service-development:voice-service',
                    voice_service_id = session.service.id,
                     session_id = session.id)
        else:
            raise ValueError('Incorrect request: Caller ID and/or Session ID and/or language ID not set, required for registration of user')

    def get(self, request):
        #If GET and caller_id and session_id are provided, present registration VoiceXML 'form'
        if set(('caller_id', 'session_id')) <= set(request.GET):
            session = get_object_or_404(CallSession, pk = request.GET['session_id'])
            caller_id = request.GET['caller_id']
            return user_registration_form(request, session, caller_id)


        #If incorrect GET/POST parameters are provided, raise error
        else:
            raise ValueError('Incorrect request: Caller ID and/or Session ID not set, required for registration form')

