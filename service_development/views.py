from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse

from .models import Choice, CallSession
# Create your views here.

def index(request):
    return HttpResponse('This is the VoiceXML generator')

def choice(request, element_id, session_id):
    choice_element = get_object_or_404(Choice, pk=element_id)
    session = CallSession()
    language = session.get_language()
    choice_element_with_voice_labels = choice_element.get_choice_and_options(language)
    context = {'choice':choice_element,
                'choice_voice_label':choice_element_voice_label,
                'choice_options':choice_options[0],
                'choice_options_voice_labels':choice_options[1]}
    return render(request, 'choice.xml', context, content_type='text/xml')
