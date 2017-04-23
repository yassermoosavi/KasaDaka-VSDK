from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect

def language_selection(request, voice_service_id, session_id):
    context = {}
    return render(request, 'user_registration.xml', context, content_type='text/xml')
