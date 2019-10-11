from django.shortcuts import render
from records.models import Student, Lesson, Notification


def studentlist(request):
    students = Student.objects.filter(teacher=request.user)
    return render(request, "classic/studentlist.html",
                  {'activetab': 'students',
                   'students': students})


def lessonlist(request):
    return render(request, "classic/lessonlist.html", {'activetab': 'lessons'})
