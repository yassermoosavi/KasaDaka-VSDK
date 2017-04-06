from django.contrib import admin
from .models import Language, VoiceLabel, VoiceFragment



class VoiceLabelInline(admin.TabularInline):
    model = VoiceFragment
    extra = 2
    fk_name = 'parent'

class VoiceLabelAdmin(admin.ModelAdmin):
    inlines = [VoiceLabelInline]


# Register your models here.
admin.site.register(Language)
admin.site.register(VoiceLabel, VoiceLabelAdmin)
