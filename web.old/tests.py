from django.db.utils import IntegrityError
from django.test import TestCase
from .models import Song, Artist
from django.utils import timezone
from time import time


class ArtistTests(TestCase):
    def test_name_is_unique(self):
        name = 'a'
        a = Artist.objects.create(name=name)
        with self.assertRaises(IntegrityError):
            b = Artist.objects.create(name=name)


# Create your tests here.
class SongTests(TestCase):
    def test_string_represenation_is_song_name_by_artist_name(self):
        artist_name = "Maor"
        song_name = "Test"
        a = Artist.objects.create(name=artist_name)
        s = Song.objects.create(artist=a, name=song_name)
        self.assertEqual("{0} by {1}".format(song_name, artist_name), s.__str__())

    def test_unique_key_name__artist_name(self):
        artist_name = "Nirvana"
        song_name = "All Apologies"
        a = Artist.objects.create(name=artist_name)
        s = Song.objects.create(artist=a, name=song_name)
        with self.assertRaises(IntegrityError):
            s2 = Song.objects.create(artist=a, name=song_name)





