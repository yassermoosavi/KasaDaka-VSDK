from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse


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
    from django.urls import reverse 
    from django.http import HttpResponseRedirect
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return HttpResponseRedirect(url + "?%s" % params)

def reverse_add_get_parameters(url_name, *args, **kwargs):
    """
    Like Django's reverse(), but adds GET parameters at the end of the URL.
    """
    from django.core.urlresolvers import reverse 
    import urllib
    url = reverse(url_name, args = args)
    params = urllib.parse.urlencode(kwargs)
    return url + "?%s" % params

def user_login(request):
    template = loader.get_template('user/user_login.html')
    return HttpResponse(template.render({}, request))
	
def call_data(request, session_id):
    from ..models import CallSession, CallSessionStep, VoiceServiceSubElement
    call_session = CallSession.objects.all()
    call_session_details = CallSessionStep.objects.filter(session_id = session_id)
    call_session_steps = CallSessionStep.objects.get(session_id = session_id, id__in = [72, 68, 60, 64])
    message = ''
	
    if call_session_steps.id == 72:
	    message = 'Based on the answers provided, Infectious Bursal disease diagnosed!'
	
    elif call_session_steps.id == 68:
	    message = 'Based on the answers provided, New Castle disease diagnosed!' 

    elif call_session_steps.id == 60:
	    message = 'Based on the answers provided, Fowl Pox disease diagnosed!'
		
    elif call_session_steps.id == 64:
	    message = 'Based on the answers provided, Mareks disease diagnosed!'
		
    else:
	    message = 'Based on the answers provided, no disease could be diagnosed!'
	
    return render(request, 'user/call_data.html', {'call_session':call_session, 'message': message, 'call_session_details':call_session_details})
	
def session_list(request):
	from ..models import CallSession
	call_session_list = CallSession.objects.all()
	return render(request, 'user/dashboard.html', {'call_session_list': call_session_list})
