from django.db import models

from .vs_element import VoiceServiceElement

class Choice(VoiceServiceElement):
    _urls_name = 'service-development:choice'

    def __str__(self):
        return self.name

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self):
        #TODO: check all children (choice options)
        
        if self.voice_label:
            return self.voice_label.validator()
        else:
            return ['No VoiceLabel in element: "%s"'%self.name]  


    #def get_absolute_url(self, **kwargs):
    #    """
    #    Give the URL to reach this Choice, arguments must match those in urls.py
    #    """
    #    return reverse('service_development:choice')
    #    return reverse('service_development:choice', kwargs= {'element_id':'str(self.id)'})

class ChoiceOption(VoiceServiceElement):
    parent = models.ForeignKey(
            Choice,
            #TODO: controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
            related_name='choice_options')
    _redirect = models.ForeignKey(
            VoiceServiceElement, 
            #TODO: controlerne of dit wel echt cascade moet zijn???
            on_delete = models.CASCADE,
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
        #check if voice label is present
        if self.voice_label:
            errors.extend(self.voice_label.validator())
        else:
            errors.append('No VoiceLabel in choice option: "%s"'%self.name)

        #check if redirect is present
        if not self._redirect:
            errors.append('No redirect in choice option: "%s"'%self.name)
        #check whether element that will be redirected to is appointed to the same voice service
        #elif not self.redirect in self.service.get_elements():
        #    errors.append('Redirect "%s" in choice option "%s" does not belong to same voice service'% (self.redirect.name, self.name))

        return errors

