from django.urls import path
from . import views

app_name = "records"

"""
    path('students/', views.students),
    path('students/
    path('lessons/<int:year>/<int:month>/', views.students),
"""

urlpatterns = [
    path('students/', views.StudentList.as_view(), name="student_list"),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name="student_detail"),
]
