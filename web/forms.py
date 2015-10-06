from django.forms import ModelForm
from .models import Song


class EditForm(ModelForm):

    class Meta:
        model = Song
        fields = ('name', 'artist', 'video', 'lesson_video', 'chords_text', 'chords_url', 'tabs_text', 'tabs_url')
