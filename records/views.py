from django.shortcuts import render
from django.core.serializers import serialize
from django.http import JsonResponse
from records.models import Student, Lesson

def students(request):
    if request.user.id:
        students_py = serialize('python', Student.objects.filter(teacher=request.user.id))
        field_data = [d['fields'] for d in students_py]
        return JsonResponse({"status": "OK", "students": field_data})
    else:
        return JsonResponse({"status": "You must be logged in."})
