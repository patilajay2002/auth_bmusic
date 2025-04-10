from django.contrib import admin
from .models import Artist, Album, Music, Playlist,Language,AddedTrack

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Music)
admin.site.register(Playlist)
admin.site.register(Language)
admin.site.register(AddedTrack)