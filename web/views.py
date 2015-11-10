from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from .models import Song, Artist, Comment
from .forms import SongForm, RegisterForm, ArtistForm, CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.utils.decorators import method_decorator

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
        form = SongForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = SongForm(instance=song)
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
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save(commit=False)
            song.create_user = request.user
            song.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = SongForm()
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
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

