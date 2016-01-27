from django.contrib.auth.models import User
from rest_framework import serializers
from web.models import Song, Artist, Genre


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Artist

class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre