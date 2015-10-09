from django.forms import ModelForm
from .models import Song
from django.contrib.auth.models import User


class EditForm(ModelForm):

    class Meta:
        model = Song
        fields = ('name', 'artist', 'video', 'lesson_video', 'chords_text', 'chords_url', 'tabs_text', 'tabs_url')


class RegisterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


