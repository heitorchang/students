from django.urls import path
from . import views

app_name = "ui"

urlpatterns = [
    path('students/', views.studentform),
]
