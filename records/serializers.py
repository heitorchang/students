from rest_framework import serializers
from .models import Student, Lesson

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'phone', 'email', 'lesson_weekday', 'lesson_time']
