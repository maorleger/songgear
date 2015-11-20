from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField


class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Song(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    artist = models.ForeignKey(Artist, blank=False, null=False)
    video = EmbedVideoField(null=True, blank=True)
    lesson_video = EmbedVideoField(null=True, blank=True)
    chords_text = models.TextField(null=True, blank=True)
    chords_url = models.URLField(null=True, blank=True)
    tabs_text = models.TextField(null=True, blank=True)
    tabs_url = models.URLField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    create_user = models.ForeignKey(User, blank=False, null=False)
    genre = models.ForeignKey(Genre, blank=True, null=True)


    def __str__(self):
        return "{0} by {1}".format(self.name, self.artist.name)

    class Meta:
        unique_together = ('artist', 'name', 'create_user')


class Comment(models.Model):
    song = models.ForeignKey(Song, blank=False, null=False)
    create_user = models.ForeignKey(User, blank=False, null=False)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.comment
