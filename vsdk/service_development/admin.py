from django.contrib import admin
from django.utils.translation import gettext as _


from .models import VoiceService, MessagePresentation, Choice, ChoiceOption, VoiceFragment, CallSession, CallSessionStep, KasaDakaUser, Language, VoiceLabel

def format_validation_result(obj):
        """
        Creates a HTML list from all errors found in validation
        """
        return '<br/>'.join(obj.validator())


class VoiceServiceAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : ['name', 'description', 'vxml_url', 'active', 'is_valid', 'validation_details', 'supported_languages']}),
                    ('Registration process', {'fields': ['registration', 'registration_language', 'registration_name']}),
                    ('Call flow', {'fields': ['_start_element']})]
    list_display = ('name','active','is_valid')
    readonly_fields = ('vxml_url', 'is_valid', 'validation_details')

    def get_readonly_fields(self, request, obj=None):
        """
        Only allow activation of voice service if it is valid
        """
        if obj is not None:
            if not obj.is_valid():
                return self.readonly_fields + ('active',)
        return self.readonly_fields


    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True
    

class VoiceServiceElementAdmin(admin.ModelAdmin):
    fieldsets = [('General',    {'fields' : [ 'name', 'description','service','is_valid', 'validation_details', 'voice_label']})]
    list_filter = ['service']
    list_display = ('name', 'service', 'is_valid')
    readonly_fields = ('is_valid', 'validation_details')
     
    def validation_details(self, obj=None):
        return format_validation_result(obj)
    validation_details.allow_tags = True

class ChoiceOptionsInline(admin.TabularInline):
    model = ChoiceOption
    extra = 2
    fk_name = 'parent'
    view_on_site = False

class ChoiceAdmin(VoiceServiceElementAdmin):
    inlines = [ChoiceOptionsInline]

class VoiceLabelInline(admin.TabularInline):
    model = VoiceFragment
    extra = 2
    fk_name = 'parent'

class VoiceLabelByVoiceServicesFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Voice Service')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'voice-service'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        voice_services  = VoiceService.objects.all()
        result = []
        for service in voice_services:
            result.append((service.id,service.name))
        return result

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return VoiceLabel.objects.filter(voiceservicesubelement__service__id=self.value()).distinct()

class VoiceLabelAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = [VoiceLabelByVoiceServicesFilter]
    inlines = [VoiceLabelInline]




class CallSessionInline(admin.TabularInline):
    model = CallSessionStep
    extra = 0 
    fk_name = 'session'
    can_delete = False
    fieldsets = [('General', {'fields' : ['visited_element', 'time', 'description']})]
    readonly_fields = ('time','session','visited_element', 'description')
    max_num = 0

class CallSessionAdmin(admin.ModelAdmin):
    list_display = ('start','user','service','caller_id','language')
    list_filter = ('service','user','caller_id')
    fieldsets = [('General', {'fields' : ['service', 'user','caller_id','start','end','language']})]
    readonly_fields = ('service','user','caller_id','start','end','language') 
    inlines = [CallSessionInline]
    can_delete = False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, reques, obj=None):
        return False

    def get_actions(self, request):
        actions = super(CallSessionAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

class MessagePresentationAdmin(VoiceServiceElementAdmin):
    fieldsets = VoiceServiceElementAdmin.fieldsets + [('Message Presentation', {'fields': ['_redirect','final_element']})]

class KasaDakaUserAdmin(admin.ModelAdmin):
    list_filter = ['service','language','caller_id']
    list_display = ('__str__','caller_id', 'service', 'language')

# Register your models here.

admin.site.register(VoiceService, VoiceServiceAdmin)
admin.site.register(MessagePresentation, MessagePresentationAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(CallSession, CallSessionAdmin)
admin.site.register(KasaDakaUser, KasaDakaUserAdmin)
admin.site.register(Language)
admin.site.register(VoiceLabel, VoiceLabelAdmin)
