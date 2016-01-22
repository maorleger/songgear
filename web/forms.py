from crispy_forms.bootstrap import FormActions, FieldWithButtons, StrictButton
from django import forms
from django.core.urlresolvers import reverse
from django.forms import ModelForm, BooleanField, HiddenInput
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
        self.helper.add_input(Submit('submit', 'submit', css_class='btn'))
    class Meta:
        model = Artist
        fields = ('name',)



class SongForm(ModelForm):

    public = BooleanField(label="Allow other users to edit this song?", required=False)

    def __init__(self, user, *args, **kwargs):
        super(SongForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                '',
                'public',
                FieldWithButtons ('genre', StrictButton("Add new", name="toggle_new_genre", css_class="toggleButton", data_div_id="new_genre_div")),
                HTML("""<div id="new_genre_div" style="display:none;" class="input-group">
                        {% csrf_token %}
                        <input type="text" id="new_genre" name="new_genre" placeholder="Genre..." class="textinput textInput form-control" maxlength="200" />
                        <span class="input-group-btn"><input type="button" name="submit" value="submit" id="add_genre" class="btn btn-primary btn"></span>
                        </div>
                """),
                'name',
                FieldWithButtons('artist', StrictButton("Add new", name="toggle_new_artist" , css_class="toggleButton", data_div_id="new_artist_div")),


                HTML("""<div id="new_artist_div" style="display:none;" class="input-group">
                        {% csrf_token %}
                        <input type="text" id="new_artist" name="new_artist" placeholder="Artist name..." class="textinput textInput form-control" maxlength="200" />
                        <span class="input-group-btn"><input type="button" name="submit" value="submit" id="add_artist" class="btn btn-primary btn"></span>
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
            # in this case we are editing a song
            if kwargs['instance'].create_user != user:
                self.fields['public'].widget = HiddenInput()
        except KeyError:
            self.helper.form_action = reverse('web:new')


    class Meta:
        model = Song
        fields = ('genre', 'name', 'artist', 'public', 'video', 'lesson_video', 'chords_text', 'chords_url', 'tabs_text', 'tabs_url')


class RegisterForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('web:register')

        self.helper.add_input(Submit('register', 'Register!', css_class='btn'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.is_active = False
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')

