from django.db import models


class VoiceLabel(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank = True, null = True)

    def __str__(self):
        return "Voice Label: %s" % (self.name)

    def is_valid(self):
        return len(self.validator()) == 0
    is_valid.boolean = True

    def validator(self, language):
        errors = []        
        if len(self.voicefragment_set.filter(language = language)) > 0:
            errors.extend(self.voicefragment_set.filter(language=language)[0].validator())
        else:
            errors.append('"%s" does not have a Voice Fragment for "%s"'%(str(self),str(language)))
        return errors

    def get_voice_fragment_url(self, language):
        return self.voicefragment_set.filter(language=language)[0].get_url()

class Language(models.Model):
    name = models.CharField(max_length=100, unique = True)
    code = models.CharField(max_length=10, unique = True)
    voice_label = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_description_voice_label',
            help_text = "A Voice Label of the name of the language")
    error_message = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_error_message',
            help_text = "A general error message")
    select_language = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_select_language',
            help_text = "A message requesting the user to select a language")
    pre_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_pre_choice_option',
            help_text = "The fragment that is to be played before a choice option (e.g. '[to select] option X, please press 1')")
    post_choice_option = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_post_choice_option',
            help_text = "The fragment that is to be played before a choice option (e.g. 'to select option X, [please press] 1')")
    one = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_one',
            help_text = "The number 1")
    two = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_two',
            help_text = "The number 2")
    three = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_three',
            help_text = "The number 3")
    four = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_four',
            help_text = "The number 4")
    five = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_five',
            help_text = "The number 5")
    six = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_six',
            help_text = "The number 6")
    seven = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_seven',
            help_text = "The number 7")
    eight = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_eight',
            help_text = "The number 8")
    nine = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_nine',
            help_text = "The number 9")
    zero = models.ForeignKey('VoiceLabel',
            on_delete = models.PROTECT,
            related_name = 'language_zero',
            help_text = "The number 0")

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

    @property
    def get_description_voice_label_url(self):
        """
        Returns the URL of the Voice Fragment describing
        the language, in the language itself.
        """
        return self.voice_label.get_voice_fragment_url(self)

    @property
    def get_interface_numbers_voice_label_url_list(self):
        numbers = [
                    self.zero,
                    self.one,
                    self.two,
                    self.three,
                    self.four,
                    self.five,
                    self.six,
                    self.seven,
                    self.eight,
                    self.nine
                    ]
        result = []
        for number in numbers:
            result.append(number.get_voice_fragment_url(self))
        return result

    @property
    def get_interface_voice_label_url_dict(self):
        """
        Returns a dictionary containing all URLs of Voice
        Fragments of the hardcoded interface audio fragments.
        """
        interface_voice_labels = {
                'voice_label':self.voice_label,
                'error_message':self.error_message,
                'select_language':self.select_language,
                'pre_choice_option':self.pre_choice_option,
                'post_choice_option':self.post_choice_option,
                }
        for k, v in interface_voice_labels.items():
            interface_voice_labels[k] = v.get_voice_fragment_url(self)
        return interface_voice_labels



class VoiceFragment(models.Model):
    parent = models.ForeignKey('VoiceLabel',
            on_delete = models.CASCADE)
    language = models.ForeignKey(
            'Language',
            on_delete = models.CASCADE)
    audio = models.FileField(
            help_text = "Ensure your file is in the correct format! Wave: Sample rate 8KHz, 16 bit, mono, Codec: PCM 16 LE (s16l)")

    def __str__(self):
        return "Voice Fragment: (%s) %s" % (self.language.name, self.parent.name)

    def get_url(self):
        return self.audio.url

    def validator(self):
        errors = []
        #TODO add some real wav file validation here?
        if not self.audio:
            errors.append('%s does not have an audio file'%str(self))
        return errors


