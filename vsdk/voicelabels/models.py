from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

class VoiceLabel(models.Model):
    name = models.CharField(max_length=50)
    language = models.ForeignKey(
            Language,
            on_delete = models.CASCADE)
    placeholderFileURL = models.CharField(max_length=50)

    def __str__(self):
        return "(%s): %s" % (self.language.code , self.name)
