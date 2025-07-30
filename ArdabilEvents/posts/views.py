from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CreatePostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CreatePost
from rest_framework.parsers import MultiPartParser, FormParser
import os

class PostCrudView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self,request):
        posts = CreatePost.objects.filter(user=request.user)
        serializer = CreatePostSerializer(posts, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        serializer = CreatePostSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,201)
        return Response(serializer.errors,400)
    
    def delete(self,request):
        post_id = request.data.get("postid")

        if post_id is None:
            return Response({"error": "postid is required."}, status=400)
        try:
            post_id = int(post_id)
        except (ValueError, TypeError):
            return Response({"error": "postid must be an integer."}, status=400)

        try:
            post = CreatePost.objects.get(id=post_id)
        except CreatePost.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

        if post.user != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=403)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=204)

    def put(self, request):
        post_id = request.data.get("postid")

        if post_id is None:
            return Response({"error": "postid is required."}, status=400)
        try:
            post_id = int(post_id)
        except (ValueError, TypeError):
            return Response({"error": "postid must be an integer."}, status=400)

        try:
            post = CreatePost.objects.get(id=post_id)
        except CreatePost.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

        if post.user != request.user:
            return Response({"error": "You do not have permission to update this post."}, status=403)

        old_image = post.image

        serializer = CreatePostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()

            if "image" in request.data and old_image.name != instance.image.name:
                if old_image and os.path.isfile(old_image.path):
                    os.remove(old_image.path)

            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
class LastFiftyPost(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        posts = CreatePost.objects.all().order_by('-created_at')[:50]
        serializer = CreatePostSerializer(posts, many=True)
        return Response(serializer.data, status=200)