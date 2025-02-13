from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from chat.models import Message

User = get_user_model()

class ChatTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.message = Message.objects.create(sender=self.user1, receiver=self.user2, room_name="testroom", content="Hello!")

    def test_fetch_chat_history(self):
        self.client.force_login(self.user1)
        response = self.client.get(f"/api/chat/messages/testroom/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["content"], "Hello!")

    def test_unauthenticated_cannot_fetch_messages(self):
        response = self.client.get(f"/api/chat/messages/testroom/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
