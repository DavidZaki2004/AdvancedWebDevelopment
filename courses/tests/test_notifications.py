from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Notification

User = get_user_model()

class NotificationTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="password123", is_teacher=True)
        self.student = User.objects.create_user(username="student", password="password123", is_student=True)
        self.notification = Notification.objects.create(user=self.teacher, message="New student enrolled")

    def test_fetch_notifications(self):
        self.client.force_login(self.teacher)
        response = self.client.get("/api/courses/notifications/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthenticated_cannot_fetch_notifications(self):
        response = self.client.get("/api/courses/notifications/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
