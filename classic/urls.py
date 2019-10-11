from django.urls import path
from . import views

app_name = 'classic'

urlpatterns = [
    # create one, read all
    path('students/', views.studentlist, name="studentlist"),

    # read one, update one
    path('students/<int:student_id>/', views.studentdetail, name="studentdetail"),

    # create one, read all
    path('lessons/', views.lessonlist, name="lessonlist"),
]

"""

    # delete one
    path('students/<int:student_id>/confirm_delete/', views.studentconfirmdelete, name="studentconfirmdelete"),
    path('students/<int:student_id>/delete/', views.studentdelete, name="studentdelete"),

"""