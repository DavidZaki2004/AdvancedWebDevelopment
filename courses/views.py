from rest_framework import generics, permissions
from .models import Course, Enrollment, Feedback, Notification
from .serializers import CourseSerializer, EnrollmentSerializer, FeedbackSerializer, NotificationSerializer
from users.permissions import IsTeacher, IsStudent
from django.core.mail import send_mail
from .models import Notification

# View for Teachers to create courses
class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)  # Assign logged-in teacher

# View for listing all courses
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated] # Ensure authenticated users can view

# View for Students to enroll in a course
class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)  # Assign logged-in student

class FeedbackCreateView(generics.CreateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)  # Assign logged-in student

class FeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        course_id = self.kwargs['course_id']
        return Feedback.objects.filter(course_id=course_id)

class EnrollmentCreateView(generics.CreateAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        enrollment = serializer.save(student=self.request.user)
        teacher = enrollment.course.teacher

        # Create a notification for the teacher
        Notification.objects.create(
            user=teacher,
            message=f"Student {self.request.user.username} has enrolled in your course {enrollment.course.title}."
        )

        # Send email to the teacher
        send_mail(
            "New Enrollment Notification",
            f"Student {self.request.user.username} has enrolled in your course {enrollment.course.title}.",
            "noreply@elearning.com",
            [teacher.email],
            fail_silently=True
        )

class CourseMaterialUploadView(generics.CreateAPIView):
    serializer_class = CourseSerializer  # Assuming material is uploaded with course update
    permission_classes = [permissions.IsAuthenticated, IsTeacher]

    def perform_create(self, serializer):
        course = serializer.save()
        students = [enrollment.student for enrollment in course.enrollments.all()]

        for student in students:
            Notification.objects.create(
                user=student,
                message=f"New materials have been uploaded for {course.title}."
            )

            # Send email to students
            send_mail(
                "Course Update Notification",
                f"New materials have been uploaded for {course.title}.",
                "noreply@elearning.com",
                [student.email],
                fail_silently=True
            )

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)
