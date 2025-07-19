from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re

class UserSignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "username and password are required."}, status=400)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters long."}, status=400)
        if len(password) > 128:
            return Response({"error": "Password must be at most 128 characters long."}, status=400)

        if len(username) < 8:
            return Response({"error": "username must be at least 8 characters long."}, status=400)
        if len(username) > 128:
            return Response({"error": "username must be at most 128 characters long."}, status=400)

        if not re.match(r'^[\w.@+-]+$', username):
            return Response({"error": "username contains invalid characters."}, status=403)

        if User.objects.filter(username=username).exists():
            return Response({"error": "A user with this username already exists."}, status=409)

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()

        return Response({"info": "account created successfully."}, status=201)