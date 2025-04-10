from django.shortcuts import render
from django.db.models import Count
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status,permissions
from  .serializers import  RegisterSerializer,LoginSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Artist, Language, Album, Music, Playlist,AddedTrack
from .serializers import ArtistSerializer, LanguageSerializer, AlbumSerializer, MusicSerializer, PlaylistSerializer,AddedTrackSerializer
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here. 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_music(request):
    musics=Music.objects.all().order_by('-release_date')
    serializer=MusicSerializer(musics,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_playlist(request):
    playlist=Playlist.objects.annotate(song_count=Count('songs')).filter(song_count__gt=3).order_by('-song_count')
    serializer=PlaylistSerializer(playlist,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def add_track(request):
    addTrack=AddedTrack.objects.all().order_by('-added_at')
    serializer=AddedTrackSerializer(addTrack,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


# search
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def all_music_search(request):
    query = request.GET.get('q', '') 
    music_serializer=None
    if query:
        query=query[:len(query)-1]
        music_results = Music.objects.filter(title__icontains=query.upper())
        music_serializer = MusicSerializer(music_results, many=True)
    return Response(music_serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def all_playlist_search(request):
    query = request.GET.get('q', '') 
    playlist_serializer=None
    if query:
        query=query[:len(query)-1]
        playlist__results =Playlist.objects.filter(name__icontains=query.upper())
        playlist_serializer = PlaylistSerializer(playlist__results, many=True)
    return Response(playlist_serializer.data,status=status.HTTP_200_OK)

# Authentication 
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.save()
        
        return Response({
            "message":"User registered successfully!",
            "user":RegisterSerializer(user).data,
        },
        status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer=LoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data,
        status=status.HTTP_200_OK
        )
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_view(request):
    serializer=UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        refresh=request.data.get("refresh")
        if not refresh:
            return Response({"error":"Refresh Token is Required !"},status=status.HTTP_400_BAD_REQUEST)
        token=RefreshToken(refresh)
        token.blacklist()
        return Response({"message":"Logout successfully!"},status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    