from django.db import models
from django.conf import settings

from django.utils import timezone
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
        from django.template import defaultfilters
        date = defaultfilters.date(self.time, "SHORT_DATE_FORMAT")
        time = defaultfilters.time(self.time, "TIME_FORMAT")
        return 'Spoken User Input: %s @ %s %s by %s (%s)'%(self.category.name, str(date), str(time), str(self.session.caller_id), self.session.service.name)


    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')




