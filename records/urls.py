from django.urls import path
from . import views

app_name = "records"

urlpatterns = [
    path('students/', views.students),
]
