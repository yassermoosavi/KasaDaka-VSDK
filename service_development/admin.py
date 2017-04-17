from django.contrib import admin
from .models import VoiceService, MessagePresentation, Choice, ChoiceOption, CallSession, KasaDakaUser




class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : ['active', 'is_valid', 'validation_details', 'name', 'description', 'supported_languages']}),
                    ('Call flow', {'fields': ['_start_element']})]
    list_display = ('name','active','is_valid')
    readonly_fields = ('is_valid', 'validation_details')

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid():
                return self.readonly_fields + ('active',)
        return self.readonly_fields

    def validation_details(self, obj=None):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())
    validation_details.allow_tags = True
    

class VoiceServiceElementAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : [ 'is_valid', 'validation_details', 'name', 'description', 'voice_label']})]
    list_display = ('name', 'is_valid')
    readonly_fields = ('is_valid', 'validation_details')
     
    def validation_details(self, obj=None):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())
    validation_details.allow_tags = True

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    extra = 2
    fk_name = 'parent'

class ChoiceAdmin(VoiceServiceElementAdmin):
    inlines = [ChoiceOptionsInline]



# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(CallSession)
admin.site.register(KasaDakaUser)
