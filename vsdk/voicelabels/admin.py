from django.contrib import admin
from .models import Language, VoiceLabel

# Register your models here.
admin.site.register(Language)
admin.site.register(VoiceLabel)
