from django.db import models
from django.db.models.functions import Lower
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

    class Meta:
        ordering = ['teacher', Lower('name')]
        
    def __str__(self):
        return "{} ({})".format(self.name, self.teacher)

    
class Lesson(models.Model):
    teacher = models.ForeignKey(User, related_name="records_lessons", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="records_lessons", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    notified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['teacher', 'start_at']
        
    def __str__(self):
        return "{} {} to {}".format(self.student, format_lesson_time(self.start_at), format_lesson_time(self.end_at))


class Notification(models.Model):
    teacher = models.ForeignKey(User, related_name="records_notifications", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField()
    is_new = models.BooleanField(default=True)

    class Meta:
        ordering = ['teacher', '-is_new', 'due_at']

    def __str__(self):
        return "{} due {} {}".format(self.message, format_lesson_time(self.due_at), "[unread]" if self.is_new else "")
