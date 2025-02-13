from django.urls import path
from .views import CourseCreateView, CourseListView, EnrollmentCreateView, FeedbackCreateView, FeedbackListView, NotificationListView

urlpatterns = [
    path('create/', CourseCreateView.as_view(), name='create_course'),  # Teachers create courses
    path('list/', CourseListView.as_view(), name='list_courses'),  # List all courses
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll_course'),  # Students enroll
    path('<int:course_id>/feedback/', FeedbackListView.as_view(), name='course_feedback'),
    path('feedback/create/', FeedbackCreateView.as_view(), name='create_feedback'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),

]
