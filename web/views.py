from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Song, Artist, Comment, Genre, UserProfile
from .forms import SongForm, RegisterForm, ArtistForm, CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.core.mail import send_mail, EmailMessage
import hashlib, random, datetime
from django.contrib.auth.models import User


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


def index(request):
    return render(request, 'web/index.html')


@login_required
def detail(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_user = request.user
            comment.song = song
            comment.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = CommentForm()
    return render(request, 'web/detail.html', {'song': song, 'form': form})


@login_required
def delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    song.delete()
    return HttpResponseRedirect(reverse('web:songs'))


@login_required
def delete_comment(request, pk, comment):
    comment = get_object_or_404(Comment, pk=comment)
    comment.delete()
    return HttpResponseRedirect(reverse('web:detail', args=(pk,)))


@login_required
def copy(request, pk):
    song = get_object_or_404(Song, pk=pk)

    # try to find my copy of this song first, otherwise create it
    q = Q(artist=song.artist) & Q(name=song.name) & Q(create_user=request.user)
    mycopy = Song.objects.filter(q)

    if len(mycopy) == 0:
        song.pk = None
        song.create_user = request.user
        song.save()
    else:
        song = mycopy[0]

    return HttpResponseRedirect(reverse('web:detail', args=(song.pk,)))


@login_required
def edit(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = SongForm(request.user, request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = SongForm(request.user, instance=song)
    return render(request, 'web/form.html', {'form': form, 'pk': pk})


@login_required
def edit_artist(request, pk):
    artist = get_object_or_404(Artist, pk=pk)
    if request.method == 'POST':
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save()
            return HttpResponseRedirect(reverse('web:songs'))
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'web/form.html', {'form': form, 'pk': pk})


@login_required
def new(request):
    if request.method == 'POST':
        form = SongForm(request.user, request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.create_user = request.user
            song.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = SongForm(request.user)
    return render(request, 'web/form.html', {'form': form})


@login_required
def new_artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save()
            return HttpResponseRedirect(reverse('web:songs'))
    else:
        form = ArtistForm()
    return render(request, 'web/new.html', {'form': form})


@login_required
def new_artist_ajax(request):
    if request.method == 'POST':
        artist_name = request.POST['new_artist']
        artist = Artist.objects.all().filter(name=artist_name)

        if artist.count() == 1:
            artist = artist[0]
        else:
            artist = Artist.objects.create(name=artist_name)

        return JsonResponse({"id": artist.id, "name": artist.name})


@login_required
def new_genre_ajax(request):
    if request.method == 'POST':
        genre_name = request.POST['new_genre']
        genre = Genre.objects.all().filter(name=genre_name)

        if genre.count() == 1:
            genre = genre[0]
        else:
            genre = Genre.objects.create(name=genre_name)

        return JsonResponse({"id": genre.id, "name": genre.name})


@login_required
def artists(request):
    artists = Artist.objects.all().order_by('name')
    return render(request, 'web/artists.html', {'artist_list': artists})


@login_required
def songs(request):
    songs = Song.objects.all().order_by('name')

    # return a filtered list based on search pattern
    try:
        search_term = request.GET['search']
    except KeyError:
        search_term = ""

    q = Q(name__icontains=search_term) | Q(artist__name__icontains=search_term)
    songs = songs.filter(q).order_by('artist__name', 'name')

    if search_term != "" and len(songs) == 1:
        return HttpResponseRedirect(reverse('web:detail', args=(songs[0].id,)))

    return render(request, 'web/songs.html', {'song_list': songs})




def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            # create a unique activation key
            salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
            activation_key = hashlib.sha1(str(salt+email).encode('utf-8')).hexdigest()

            # get the user from db and create a new user profile with activation key
            user = User.objects.get(username=username)
            new_profile = UserProfile(user=user, activation_key=activation_key)
            new_profile.save()

            # send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey {0}, thanks for signing up with SongGear! To activate your account, click this link: {1}".format(username, request.build_absolute_uri(reverse("web:confirm", args=(activation_key,))))

            email = EmailMessage(subject=email_subject, body=email_body, to=[email])
            email.send(fail_silently=False)

            return HttpResponseRedirect(reverse('web:register_success'))

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def register_confirm(request, activation_key):
    # check if logged in and if so redirect to home
    if request.user.is_authenticated():
        HttpResponseRedirect(reverse('web:index'))

    # check if a user profile matches activation key
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)


    # save user, set to active, and render some template
    user = user_profile.user
    user.is_active = True
    user.save()
    return render(request, 'registration/email_verified.html')

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='registration/reset_confirm.html', uidb64=uidb64, token=token,
                                  post_reset_redirect=reverse('web:login'))


def reset(request):
    return password_reset(request, template_name='registration/reset_form.html',
                          email_template_name='registration/reset_email.html',
                          post_reset_redirect=reverse('web:reset_sent'))

def reset_sent(request):
    return render(request, 'registration/reset_form.html', {'success': True})


def register_success(request):
    return render(request, 'registration/registration_success.html')
