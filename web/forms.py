from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django.core.urlresolvers import reverse
from django.forms import ModelForm, Form, CharField
from .models import Song, Artist, Comment
from django.contrib.auth.models import User
from crispy_forms.layout import Submit, Layout, Fieldset, HTML
from crispy_forms.helper import FormHelper


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)


class ArtistForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArtistForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        try:
            self.helper.form_action = reverse('web:edit_artist', args=(kwargs['instance'].id,))
        except KeyError:
            self.helper.form_action = reverse('web:new_artist')
        self.helper.add_input(Submit('submit', 'submit', css_class='btn-success'))
    class Meta:
        model = Artist
        fields = ('name',)



class SongForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'genre',
                'name',
                FieldWithButtons('artist', StrictButton("Add new", name="toggle_new_artist", id="toggle_new_artist")),


                HTML("""<div id="new_artist_div" style="display:none;">
                        {% csrf_token %}
                        <input type="text" id="new_artist" name="new_artist" placeholder="Artist name..." class="textinput textInput form-control" maxlength="200" />
                        <input type="button" name="submit" value="submit" id="add_artist" class="btn btn-primary btn-success"s>
                        </div>
                """),
                'video',
                "lesson_video",
                'chords_text',
                'chords_url',
                'tabs_text',
                'tabs_url',
            ),
            FormActions(
                Submit("submit", "submit")
            )
        )

        try:
            self.helper.form_action = reverse('web:edit', args=(kwargs['instance'].id,))
        except KeyError:
            self.helper.form_action = reverse('web:new')


    class Meta:
        model = Song
        fields = ('genre', 'name', 'artist', 'video', 'lesson_video', 'chords_text', 'chords_url', 'tabs_text', 'tabs_url')


class RegisterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('web:register')

        self.helper.add_input(Submit('register', 'Register!', css_class='btn-success'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
