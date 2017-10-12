from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from ..models import CallSession, VoiceService, Language

class LanguageSelection(TemplateView):

    def get(self, request, voice_service_id, session_id):
        """
        Asks the user to select one of the supported languages.
        """
        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = get_object_or_404(VoiceService, pk = voice_service_id)
        #get all supported languages
        languages = session.service.supported_languages.all()
        redirect_url = reverse('service-development:language-selection', args=[voice_service_id,session_id])
        context = {'languages' : languages,
                   'redirect_url' : redirect_url
                   }
        return render(request, 'language_selection.xml', context, content_type='text/xml')

    def post(self, request, voice_service_id, session_id):
        """
        Saves the chosen language to the session
        """
        if 'language_id' not in request.POST:
            #TODO return error
            return 

        session = get_object_or_404(CallSession, pk = session_id)
        voice_service = get_object_or_404(VoiceService, pk = voice_service_id) 
        language = get_object_or_404(Language, pk = request.POST['language_id'])

        session._language = language
        session.save()

        return redirect('service-development:voice-service',
                        voice_service_id = voice_service.id,
                        session_id = session.id)
