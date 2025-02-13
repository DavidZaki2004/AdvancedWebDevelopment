from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpassword123",
            "password2": "testpassword123",
            "is_student": True,
            "is_teacher": False
        }
        self.user = User.objects.create_user(username="existinguser", password="password123")

    def test_register_user(self):
        response = self.client.post("/api/users/register/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_login_user(self):
        response = self.client.post("/api/users/login/", {"username": "existinguser", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        response = self.client.post("/api/users/login/", {"username": "wronguser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_user(self):
        self.client.login(username="existinguser", password="password123")
        response = self.client.post("/api/users/logout/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
