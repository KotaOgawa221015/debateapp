from django.urls import path
from .views import TranscriptCreate, TranscriptList

urlpatterns = [
    path('transcript/', TranscriptCreate.as_view()),  # POST保存
    path('transcripts/', TranscriptList.as_view()),   # GET取得
]
