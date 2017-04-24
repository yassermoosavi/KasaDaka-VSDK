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
            if choice_option._redirect and choice_option._redirect.id == self.id:
                errors.append('!!!! There is a loop in %s'%str(choice_option))
            else:
                errors.extend(choice_option.validator())
        
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
        return VoiceServiceElement.objects.get_subclass(id = self._redirect.id)

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
            errors.extend(self.redirect.validator())

        return errors

