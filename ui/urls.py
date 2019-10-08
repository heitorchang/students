from django.urls import path
from . import views

app_name = "ui"

urlpatterns = [
    path('students/', views.studentlist),
    path('students/<int:pk>/', views.studentdetail),
    path('lessons/', views.lessonlist),
    path('lessons/<int:pk>/', views.lessondetail),
]
