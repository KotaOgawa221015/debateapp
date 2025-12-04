from django.urls import path, include
from django.contrib import admin
from django.shortcuts import render

def index(request):
    return render(request, "index.html")  # frontendを返す

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('api/', include('api.urls')),   # ← ここに集約
]
