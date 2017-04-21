from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

from ..models import VoiceService, KasaDakaUser, lookup_or_create_session, lookup_kasadaka_user_by_caller_id

from .base import *

def get_caller_id_from_GET_request(request):
    if 'caller_id' in request.GET:
        return request.GET['caller_id']
    elif 'callerid' in request.GET:
        return request.GET['callerid']
    return None


def voice_service_start(request, voice_service_id, session_id = None):
    """
    Resolves the user, else redirects to user registration VoiceXML.
    Creates a new session, then redirects to the first element of the service. 
    """
    #set/get voice_service and caller_id
    voice_service = get_object_or_404(VoiceService, pk=voice_service_id)
    caller_id = get_caller_id_from_GET_request(request) 
    session = lookup_or_create_session(voice_service, session_id, caller_id)
    
    #If the session is not yet linked to an user, try to look up the user by Caller ID, and link it to the session
    if not session.user:
        found_user = lookup_kasadaka_user_by_caller_id(caller_id, session.service)
        if found_user:
            session.link_to_user(found_user)

        # If there is no user with this caller_id, redirect to registration
        elif caller_id:
            return redirect_add_get_parameters('service-development:user-registration',
                    caller_id = caller_id,
                    session_id = session.id)

        # If the caller_id is not given, and the service requires registration,
        # raise an error
        elif not caller_id and voice_service.requires_registration:
            raise ValueError('This service requires registration, but registration is not possible, because there is no callerID!')

        # If the caller_id is not given, but the service does not require
        # registration, redirect to language selection for session only.
        elif not caller_id:

            #TODO wat als de sessie al wel een language heeft?
            return redirect('service-development:language-selection',
                    voice_service_id = voice_service.id,
                    session_id = session.id)


    
    #If user is found, redirect to starting element of voice service
    return redirect_to_voice_service_element(voice_service.start_element, session)

