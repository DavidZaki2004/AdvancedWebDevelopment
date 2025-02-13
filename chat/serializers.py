from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'room_name', 'content', 'timestamp']
