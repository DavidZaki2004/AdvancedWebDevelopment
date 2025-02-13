from django.urls import path
from .views import MessageListView
from .views import chat_room

urlpatterns = [
    path('messages/<str:room_name>/', MessageListView.as_view(), name='chat_messages'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
]
