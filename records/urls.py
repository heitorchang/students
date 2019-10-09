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
    path('lessons/', views.LessonList.as_view(), name="lesson_list"),
    path('lessons/<int:pk>/', views.LessonDetail.as_view(), name="lesson_detail"),
    path('notifications/', views.NotificationList.as_view(), name="notification_list"),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view(), name="notification_detail"),
]
