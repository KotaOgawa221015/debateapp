from django.urls import path, include
from django.contrib import admin
from api.consumers import AudioConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("api.urls")),
    path('api/', include('api.urls')),   # ← ここに集約
]
