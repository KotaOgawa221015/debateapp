from django.urls import path
from .views import TranscriptCreate, TranscriptList
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('transcript/', TranscriptCreate.as_view()),  # POST保存
    path('transcripts/', TranscriptList.as_view()),   # GET取得
]
