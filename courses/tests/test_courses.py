from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Enrollment

User = get_user_model()

class CourseTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(username="teacher", password="password123", is_teacher=True)
        self.student = User.objects.create_user(username="student", password="password123", is_student=True)
        self.course = Course.objects.create(title="Django Basics", description="Learn Django", teacher=self.teacher)

    def test_create_course(self):
        self.client.force_login(self.teacher)
        response = self.client.post(
            "/api/courses/create/",
            {"title": "New Course", "description": "Test Description"},  
            format="json",  
        )
        print("Response Data:", response.data)  # Debugging line
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_student_cannot_create_course(self):
        self.client.force_login(self.student)
        response = self.client.post("/api/courses/create/", {"title": "Unauthorized Course", "description": "Fail"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_courses(self):
        self.client.force_login(self.student)  # Login before fetching
        response = self.client.get("/api/courses/list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_enrollment(self):
        self.client.force_login(self.student)
        response = self.client.post(
            "/api/courses/enroll/",
            {"course": self.course.id},  # Ensure the course ID is passed correctly
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
