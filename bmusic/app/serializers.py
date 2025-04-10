from rest_framework import serializers
from .models import Artist, Language, Album, Music, Playlist , AddedTrack
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'  

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class MusicSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True, read_only=True)
    album = AlbumSerializer(read_only=True)
    language = LanguageSerializer(read_only=True)

    class Meta:
        model = Music
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    songs = MusicSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'
        

class AddedTrackSerializer(serializers.ModelSerializer):
    music = MusicSerializer()
    playlist = PlaylistSerializer()
    class Meta:
        model=AddedTrack
        fields='__all__'
        
# Authentication

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name","last_name", "username", "email"]
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name","last_name", "username", "email" , "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError("Invalid username or password")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }