from rest_framework import serializers
from .models import Course, Enrollment, Feedback, Notification

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'created_at']
        extra_kwargs = {'teacher': {'read_only': True}}  # Prevent user from setting teacher manually

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at']
        extra_kwargs = {'student': {'read_only': True}}  # Prevent user from setting student manually

class FeedbackSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Feedback
        fields = ['id', 'student', 'course', 'comment', 'rating', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read']
