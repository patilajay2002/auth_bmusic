"""
URL configuration for bmusic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('auth/register/',views.register_view,name="register"),
    path('auth/login/',views.login_view,name="login"),
    path('auth/logout/',views.logout_view,name="logout"),
    path('auth/user/',views.user_view,name="user"),
    
    path('get/music/', views.get_music),
    path('get/playlist/', views.get_playlist),
    path('get/track/', views.add_track),
    path('get/music/search/', views.all_music_search),
    path('get/playlist/search/', views.all_playlist_search),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
