from django.db import models
from . import CallSession, VoiceService


class UserInputCategory(models.Model):
    name = models.CharField(max_length = 100, blank = False, null = False)
    description = models.CharField(max_length = 1000, blank = True, null = True)
    service = models.ForeignKey(VoiceService, on_delete=models.CASCADE, related_name="service")


    def __str__(self):
        return '"%s" ("%s")'%(self.name, self.service.name)

class SpokenUserInput(models.Model):
    #value = models.CharField(max_length = 100, blank = True, null = True)
    audio = models.FileField(upload_to='uploads/', blank=False, null= False)
    time = models.DateTimeField(auto_now_add = True)
    session = models.ForeignKey(CallSession, on_delete=models.CASCADE, related_name="session")
    category = models.ForeignKey(UserInputCategory, on_delete=models.CASCADE, related_name="category")
    description = models.CharField(max_length = 1000, blank = True, null = True)


    def __str__(self):
        return 'Spoken User Input: "%s" @ "%s" by "%s" ("%s")'%(self.category.name, str(self.time), str(self.session.caller_id), self.session.service.name)






