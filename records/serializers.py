from rest_framework import serializers
from .models import Student, Lesson, Notification


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'phone', 'email', 'lesson_weekday', 'lesson_time', 'archived']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'student', 'start_at', 'end_at', 'notes']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'due_at', 'is_new']
