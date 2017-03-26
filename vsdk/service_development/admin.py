from django.contrib import admin
from .models import VoiceService, MessagePresentation, Choice, ChoiceOption

class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : ['active', 'name', 'description']}),
                    ('Call flow', {'fields': ['start_element']})]
    list_display = ('name','active','is_valid_voice_service','modification_date','creation_date',)

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid_voice_service():
                return self.readonly_fields + ('active',)
        return self.readonly_fields

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    extra = 2
    fk_name = 'parent'

class ChoiceAdmin(admin.ModelAdmin):
    inlines = [ChoiceOptionsInline]



# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation)
admin.site.register(Choice, ChoiceAdmin)
