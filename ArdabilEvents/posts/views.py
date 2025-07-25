from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CreatePostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CreatePostSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,201)
        return Response(serializer.errors,400)
