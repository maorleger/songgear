from django.forms import ModelForm
from .models import Song


class EditForm(ModelForm):
    class Meta:
        model = Song
        fields = '__all__'
