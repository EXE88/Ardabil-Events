from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CreatePostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CreatePost

class PostCrudView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = CreatePostSerializer(data=request.data)        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,201)
        return Response(serializer.errors,400)
    
    def delete(self,request):

        post_id = request.data.get("postid")

        # validate input data
        if post_id is None:
            return Response({"error": "postid is required."}, status=400)
        try:
            post_id = int(post_id)
        except (ValueError, TypeError):
            return Response({"error": "postid must be an integer."}, status=400)

        # Retrieve the post
        try:
            post = CreatePost.objects.get(id=post_id)
        except CreatePost.DoesNotExist:
            return Response({"error": "Post not found."}, status=404)

        # Validate owner
        if post.user != request.user:
            return Response({"error": "You do not have permission to delete this post."}, status=403)

        post.delete()
        return Response({"message": "Post deleted successfully."}, status=204)