from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse

from .models import Choice, VoiceService

from ..voicelabels.models import Language
from ..usage.models import lookup_or_create_session
from ..usage.models import KasaDakaUser
# Create your views here.

def index(request):
    return HttpResponse('This is the VoiceXML generator')

def redirect_to_voice_service_element(element,session):
    """
    Redirects to a VoiceServiceElement (of unknown subclass), including the session_id in the request.
    """
    return redirect(element._urls_name, element_id = element.id, session_id = session.id)

def redirect_add_get_parameters(url_name, *args, **kwargs):
    """
    Like Django's redirect(), but adds GET parameters at the end of the URL.
    """
    from django.core.urlresolvers import reverse 
    from django.http import HttpResponseRedirect
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)


def choice_options_resolve_redirect_urls(choice_options, session):
    choice_options_redirection_urls = []
    for choice_option in choice_options:
        redirect_url = choice_option.redirect.get_absolute_url(session)
        choice_options_redirection_urls.append(redirect_url)
    return choice_options_redirection_urls

def choice_options_resolve_voice_labels(choice_options, session):
    """
    Returns a list of voice labels belonging to the provided list of choice_options.
    """
    choice_options_voice_labels = []
    for choice_option in choice_options:
        choice_options_voice_labels.append(choice_option.get_voice_fragment_url(session))
    return choice_options_voice_labels

def choice_generate_context(choice_element, session):
    """
    Returns a dict that can be used to generate the choice VXML template
    choice = this Choice element object
    choice_voice_label = the resolved Voice Label URL for this Choice element
    choice_options = iterable of ChoiceOption object belonging to this Choice element
    choice_options_voice_labels = list of resolved Voice Label URL's referencing to the choice_options in the same position
    choice_options_redirect_urls = list of resolved redirection URL's referencing to the choice_options in the same position
        """
    choice_options =  choice_element.choice_options.all()
    context = {'choice':choice_element,
                'choice_voice_label':choice_element.get_voice_fragment_url(session),
                'choice_options': choice_options,
                'choice_options_voice_labels':choice_options_resolve_voice_labels(choice_options, session),
                    'choice_options_redirect_urls': choice_options_resolve_redirect_urls(choice_options,session),      
                    }
    return context

def choice(request, element_id, session_id):
    choice_element = get_object_or_404(Choice, pk=element_id)

    #TODO use actual sessions
    session = CallSession(id=1)
    session_step_record(session, choice_element)
    context = choice_generate_context(choice_element, session)
    
    return render(request, 'choice.xml', context, content_type='text/xml')

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
    session = lookup_or_create_session(voice_service, session_id)
    
    #If the session is not yet linked to an user, try to look up the user by Caller ID, and link it to the session
    if not session.user:
        user = KasaDakaUser.lookup_by_caller_id(caller_id, session.service)
        session.link_to_user(user)

    #If the user cannot be found (thus is not registered yet), and registration is required, redirect to registration form
    if not session.user and voice_service.requires_registration:
        return redirect_add_get_parameters('service_development:usage:user-registration',
                    caller_id = caller_id,
                    session_id = session.id)
    
    #If user is found or registration not needed, redirect to starting element of voice service
    return redirect_to_voice_service_element(voice_service.start_element, session)




