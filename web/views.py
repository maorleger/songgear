from django.shortcuts import render
from django.views import generic
from django.core.urlresolvers import reverse
from .models import Song
from .forms import EditForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q





class IndexView(generic.ListView):
    template_name = 'web/index.html'
    context_object_name = 'song_list'

    def get_queryset(self):
        return Song.objects.order_by('name')


class DetailView(generic.DetailView):
    template_name = 'web/detail.html'
    model = Song


def edit(request, pk):
    song = get_object_or_404(Song, pk=pk)
    if request.method == 'POST':
        form = EditForm(request.POST, instance=song)
        if form.is_valid():
            song = form.save()
            return HttpResponseRedirect(reverse('web:detail', args=(song.id,)))
    else:
        form = EditForm(instance=song)
    return render(request, 'web/edit.html', {'form': form, 'pk': pk})


class SongListVIew(generic.ListView):
    template_name = 'web/songs.html'
    context_object_name = 'song_list'

    def get_queryset(self):

        return Song.objects.order_by('name')

def songs(request, **kwargs):
    songs = Song.objects.all().order_by('name')

    if request.POST:
        # return a filtered list based on search pattern
        try:
            search_term = request.POST['search']
        except KeyError:
            search_term = ""

        q = Q(name__icontains=search_term) | Q(artist__name__icontains=search_term)
        songs = songs.filter(q).order_by('name')

    return render(request, 'web/songs.html', {'song_list': songs})