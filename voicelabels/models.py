from django.db import models

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)



class VoiceLabel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return "Voice Label: %s" % (self.name)

    def is_valid(self):
        return True

    def validator(self):
        return []


class VoiceFragment(models.Model):
    parent = models.ForeignKey(VoiceLabel,
            on_delete = models.CASCADE)
    language = models.ForeignKey(
            Language,
            on_delete = models.CASCADE)
    audio = models.FileField()

    def __str__(self):
        return "Voice Fragment: (%s) %s" % (self.language.name, self.parent.name)


