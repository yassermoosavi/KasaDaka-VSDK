from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import CallSession

def language_selection(request, voice_service_id, session_id):
    session = get_object_or_404(CallSession, pk = session_id)


    #get all supported languages
    languages = session.service.supported_languages.all()
    context = {'languages' : languages,
               'redirect_url' : 'bla'}
    return render(request, 'user_registration.xml', context, content_type='text/xml')
