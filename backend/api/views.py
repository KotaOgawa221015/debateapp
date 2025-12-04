from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transcript
from .serializers import TranscriptSerializer

from django.shortcuts import render

def index(request):
    return render(request, 'api/index.html')

# ==== POSTで文字起こし結果を保存 ====
class TranscriptCreate(APIView):
    def post(self, request):
        serializer = TranscriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "saved"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ==== GETで履歴を返す ====
class TranscriptList(APIView):
    def get(self, request):
        data = Transcript.objects.all().order_by('-created_at')[:50]
        return Response(TranscriptSerializer(data, many=True).data)
