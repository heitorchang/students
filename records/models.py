from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone


def format_lesson_time(t):
    return timezone.localtime(t).strftime("%d/%m/%Y %H:%M")


class Student(models.Model):
    teacher = models.ForeignKey(User, related_name="records_students", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    lesson_weekday = models.IntegerField(blank=True, null=True)  # 0 = Monday
    lesson_time = models.TimeField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name

    
class Lesson(models.Model):
    teacher = models.ForeignKey(User, related_name="records_lessons", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="records_lessons", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['start_at']
        
    def __str__(self):
        return "{} {} to {}".format(self.student, format_lesson_time(self.start_at), format_lesson_time(self.end_at))
