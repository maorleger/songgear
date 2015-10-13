from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from .models import Song, Artist
from .forms import SongForm, RegisterForm, ArtistForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.utils.decorators import method_decorator


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.order_by('name')


class DetailView(LoggedInMixin, generic.DetailView):
    template_name = 'web/detail.html'
    model = Song


@login_required
def delete(request, pk):
    song = get_object_or_404(Song, pk=pk)
    song.delete()
    return HttpResponseRedirect(reverse('web:songs'))


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
    return render(request, 'web/edit.html', {'form': form, 'pk': pk})


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
    return render(request, 'web/edit.html', {'form': form, 'pk': pk})


@login_required
def new(request):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            song = form.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = SongForm()
    return render(request, 'web/new.html', {'form': form})


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


class SongListVIew(LoggedInMixin, generic.ListView):
    template_name = 'web/songs.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.order_by('name')


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

    if len(songs) == 1:
        return render(request, 'web/detail.html', {'song': songs[0]})
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
