from django.urls import path
from . import views

app_name = 'classic'

urlpatterns = [
    # create one, read all
    path('students/', views.studentlist, name="studentlist"),

    # read one, update one
    path('students/<int:student_id>/', views.studentdetail, name="studentdetail"),

    # delete one
    path('students/<int:student_id>/confirm_delete/', views.studentconfirmdelete, name="studentconfirmdelete"),
    
    path('students/<int:student_id>/delete/', views.studentdelete, name="studentdelete"),


    # Lessons
    path('classes/', views.lessonlist, name="lessonlist"),

    # read one, update one
    path('classes/forstudent/<int:student_id>/', views.lessonforstudent, name="lessondetail"),

    # read one, update one
    path('classes/<int:lesson_id>/', views.lessondetail, name="lessondetail"),

    # delete one
    path('classes/<int:lesson_id>/confirm_delete/', views.lessonconfirmdelete, name="lessonconfirmdelete"),
    
    path('classes/<int:lesson_id>/delete/', views.lessondelete, name="lessondelete"),
]

