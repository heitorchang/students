from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'ui/index.html')


@login_required
def studentlist(request):
    return render(request, 'ui/studentlist.html')


@login_required
def studentdetail(request, pk):
    return render(request, 'ui/studentdetail.html', {'student_id': pk})


@login_required
def lessonlist(request):
    return render(request, 'ui/lessonlist.html')


@login_required
def lessondetail(request, pk):
    return render(request, 'ui/lessondetail.html', {'lesson_id': pk})
