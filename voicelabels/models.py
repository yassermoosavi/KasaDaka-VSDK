from django.db import models

# Create your models here.

class VoiceLabel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank = True, null = True)

    def __str__(self):
        return "Voice Label: %s" % (self.name)

    def is_valid(self):
        return True

    def validator(self):
        return []

    def get_voice_fragment_url(self, session):
        language = session.get_language()
        return self.voicefragment_set.filter(language=language)[0].get_url()

class Language(models.Model):
    name = models.CharField(max_length=100, unique = True)
    code = models.CharField(max_length=10, unique = True)
    voice_label = models.ForeignKey('VoiceLabel',on_delete = models.PROTECT, related_name = 'language_description_voice_label')
    error_message = models.ForeignKey('VoiceLabel',on_delete = models.PROTECT, related_name = 'language_error_message')

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

class VoiceFragment(models.Model):
    parent = models.ForeignKey('VoiceLabel',
            on_delete = models.CASCADE)
    language = models.ForeignKey(
            'Language',
            on_delete = models.CASCADE)
    audio = models.FileField()

    def __str__(self):
        return "Voice Fragment: (%s) %s" % (self.language.name, self.parent.name)

    def get_url(self):
        return self.audio.url
