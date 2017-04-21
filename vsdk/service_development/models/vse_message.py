from django.db import models

from .vs_element import VoiceServiceElement

class MessagePresentation(VoiceServiceElement):
    final_element = models.BooleanField('This element will terminate the call',default = False)
    next_element = models.ForeignKey(
            VoiceServiceElement,
            on_delete = models.SET_NULL,
            null = True,
            blank = True,
            related_name='%(app_label)s_%(class)s_related')

    def __str__(self):
        return ""
