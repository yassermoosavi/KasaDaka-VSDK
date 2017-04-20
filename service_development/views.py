from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import Choice, CallSession, CallSessionStep
# Create your views here.

def index(request):
    return HttpResponse('This is the VoiceXML generator')

def session_step_record(session, element):
    step = CallSessionStep(session = session, visited_element = element)
    step.save()
    return

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

def voice_service_start(request, voice_service_id, caller_id):
    """
    Resolves the user, else redirects to user registration VoiceXML.
    Creates a new session, then redirects to the first element of the service. 
    """
    voice_service = get_object_or_404(VoiceService, pk=voice_service_id)
    
    #try to lookup user, if user is new, redirect to user-registration
    try:
        user = KasaDakaUser.objects.get(caller_id = caller_id)
    except KasaDakaUser.DoesNotExist:
        return redirect('user-registration',
                caller_id = caller_id,
                voice_service_id = voice_service_id)

    #create new session
    session = CallSession(user = user, service = voice_service)
    session.save()

    #redirect to starting element of voice service
    return redirect(voice_service.start_element, session_id = session.id)

def user_registration(request, caller_id = None, voice_service_id = None):
    """
    Registers the user to the system
    """

    if request.method == "POST":
        #if all elements are filled, register the user
        if set(('caller_id','voice_service_id','language_id')) <= set(request.POST):
            caller_id = request.POST['caller_id']
            voice_service_id = request.POST['voice_service_id']
            language = request.POST['language_id']
    elif caller_id and voice_service_id:
        pass
    else:
        raise 

        
    voice_service = get_object_or_404(VoiceService, pk=voice_service_id)
    
    #ask user for preferred language

    user = KasaDakaUser(caller_id = caller_id,
            language = language,
            service = voice_service)
    return
