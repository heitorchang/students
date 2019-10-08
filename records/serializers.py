from rest_framework import serializers
from .models import Student, Lesson

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'phone', 'email', 'lesson_weekday', 'lesson_time']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'student', 'start_at', 'end_at', 'notes']
