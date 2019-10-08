from rest_framework import generics, permissions
from django.shortcuts import render
from .models import Student, Lesson
from .serializers import StudentSerializer, LessonSerializer
from .permissions import IsTeacher

"""
from django.core.serializers import serialize
from django.http import JsonResponse
"""


"""
def students(request):
    if request.user.id:
        students_py = serialize('python', Student.objects.filter(teacher=request.user.id))
        field_data = [d['fields'] for d in students_py]
        return JsonResponse({"status": "OK", "students": field_data})
    else:
        return JsonResponse({"status": "You must be logged in."})
"""

class StudentList(generics.ListCreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Student.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticated, IsTeacher)


class LessonList(generics.ListCreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated, IsTeacher)

    def get_queryset(self):
        return Lesson.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated, IsTeacher)
