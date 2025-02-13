from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.shortcuts import render

def chat_room(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        return Message.objects.filter(room_name=room_name).order_by("timestamp")

