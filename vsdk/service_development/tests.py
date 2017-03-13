import datetime

from django.test import TestCase
from django.utils import timezone

from .models import VoiceService

# Create your tests here.
class VoiceServiceMethodTests(TestCase):

    def test_updating_modified_date(self):
        """
        The method updateModificationDate() should update the modification_date to today.
        To test this, we will create a Voice service with a modification date in the past and update it to today.
        """
        date_in_past = timezone.now() - datetime.timedelta(days=30)
        old_voice_service = VoiceService(modification_date=date_in_past)
        old_voice_service.updateModificationDate()
        #check whether the new modification date is today (and not 30 days ago)
        mod_date_is_today = old_voice_service.modification_date >= timezone.now() - datetime.timedelta(minutes=1)
        self.assertIs(mod_date_is_today, True)
