from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from django.contrib.auth.models import update_last_login

class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            update_last_login(None, user)
            return Response(UserSerializer(user).data)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
