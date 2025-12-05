from django.urls import path, include
from django.contrib import admin
from api.consumers import StreamConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("api.urls")),
    path('api/', include('api.urls')),   # ← ここに集約
]
