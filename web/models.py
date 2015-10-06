from django.db import models
from django.forms import ModelForm

class Artist(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    artist = models.ForeignKey(Artist, blank=False, null=False)
    video = models.URLField(null=True, blank=True)
    chords_text = models.TextField(null=True, blank=True)
    chords_url = models.URLField(null=True, blank=True)
    tabs_text = models.TextField(null=True, blank=True)
    tabs_url = models.URLField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0} by {1}".format(self.name, self.artist.name)

