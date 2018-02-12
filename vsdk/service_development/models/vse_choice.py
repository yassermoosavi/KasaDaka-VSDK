from django.db import models

from .vs_element import VoiceServiceElement, VoiceServiceSubElement

class Choice(VoiceServiceElement):
    _urls_name = 'service-development:choice'

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(Choice, self).validator())
        choice_options = self.choice_options.all()
        for choice_option in choice_options:
            errors.extend(choice_option.validator())

        #deduplicate errors
        errors = list(set(errors))
        return errors


class ChoiceOption(VoiceServiceSubElement):
    parent = models.ForeignKey(
            Choice,
            on_delete = models.CASCADE,
            related_name='choice_options')
    _redirect = models.ForeignKey(
            VoiceServiceElement, 
            on_delete = models.SET_NULL,
            related_name='%(app_label)s_%(class)s_redirect_related',
            blank = True,
            null = True)

    @property
    def redirect(self):
        """
        Returns the actual subclassed object that is redirected to,
        instead of the VoiceServiceElement superclass object (which does
        not have specific fields and methods).
        """
        return VoiceServiceSubElement.objects.get_subclass(id = self._redirect.id)

    def __str__(self):
        return "(%s): %s" % (self.parent.name,self.name)
    
    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        errors = []
        errors.extend(super(ChoiceOption, self).validator())
        #check if redirect is present
        if not self._redirect:
            errors.append('No redirect in choice option: "%s"'%str(self))
        else:
            if self.service.id != self.parent.service.id:
                errors.append('Choice option "%s" not in correct (same) Voice Service as Choice element! ("%s", should be "%s")'%(str(self),str(self.service),str(self.parent.service)))
            if self.redirect.service.id != self.parent.service.id:
                errors.append('Redirect element of choice option "%s" not in correct (same) Voice Service! ("%s", should be "%s")'%(str(self),str(self.redirect.service),str(self.service)))

        return errors

