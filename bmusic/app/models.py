from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=255 , unique=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()

    def __str__(self):
        return self.title

class Music(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    release_date = models.DateField()
    genre = models.CharField(max_length=100,null=True)
    audio_file = models.FileField(upload_to='music/')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True, related_name='songs')
    image = models.ImageField(upload_to='music_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    image=models.ImageField(upload_to="playlist_images/", blank=True, null=True)
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Music, related_name='playlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AddedTrack(models.Model):
    TRACK_TYPE_CHOICES = (
        ('music', 'Music'),
        ('playlist', 'Playlist'),
    )

    track_type = models.CharField(max_length=8, choices=TRACK_TYPE_CHOICES)
    music = models.ForeignKey(Music, on_delete=models.SET_NULL, null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.SET_NULL, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.track_type == 'music':
            return f"Music '{self.music.title}' added on {self.added_at}"
        elif self.track_type == 'playlist':
            return f"Playlist '{self.playlist.name}' added on {self.added_at}"
        return "Unknown"

