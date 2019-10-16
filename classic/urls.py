from django.urls import path
from . import views

app_name = 'classic'

urlpatterns = [
    # create one, read all
    path('students/', views.studentlist, name="studentlist"),

    # read one, update one
    path('students/<int:student_id>/', views.studentdetail, name="studentdetail"),

    # display classes
    path('students/classes/<int:student_id>/', views.studentclasses, name="studentclasses"),

    # delete one
    path('students/<int:student_id>/confirm_delete/', views.studentconfirmdelete, name="studentconfirmdelete"),
    
    path('students/<int:student_id>/delete/', views.studentdelete, name="studentdelete"),


    # Lessons
    path('classes/', views.lessonlist, name="lessonlist"),

    # All Lessons
    path('classes/all/', views.lessonall, name="lessonall"),

    #  create one with selected student
    path('classes/forstudent/<int:student_id>/', views.lessonforstudent, name="lessonforstudent"),

    # read one, update one
    path('classes/<int:lesson_id>/', views.lessondetail, name="lessondetail"),

    # read one as card
    path('classes/card/<int:lesson_id>/', views.lessoncard, name="lessoncard"),

    # delete one
    path('classes/<int:lesson_id>/confirm_delete/', views.lessonconfirmdelete, name="lessonconfirmdelete"),
    
    path('classes/<int:lesson_id>/delete/', views.lessondelete, name="lessondelete"),

    # Calendars for Lessons
    # This month
    path('classes/thismonth/', views.lessonthismonth, name="lessonthismonth"),

    
    # Profile
    path('profile/', views.profile, name="profile"),
]

