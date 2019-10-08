from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'ui/index.html')


@login_required
def studentform(request):
    return render(request, 'ui/studentform.html')
