from django.contrib import admin
from .models import VoiceService, MessagePresentation, Choice, ChoiceOption

# Register your models here.

admin.site.register(VoiceService)
admin.site.register(MessagePresentation)
admin.site.register(Choice)
admin.site.register(ChoiceOption)
