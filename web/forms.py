from django.core.urlresolvers import reverse
from django.forms import ModelForm
from .models import Song
from django.contrib.auth.models import User
from crispy_forms.layout import Submit
from crispy_forms.helper import FormHelper


class NewEditForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        try:
            self.helper.form_action = reverse('web:edit', args=(kwargs['instance'].id,))
        except KeyError:
            self.helper.form_action = reverse('web:new')
        # self.helper.form_action = reverse('web:detail', args=(Song.id,))
        self.helper.add_input(Submit('submit', 'submit', css_class='btn btn-success'))

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


