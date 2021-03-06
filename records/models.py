from django.db import models
from django.db.models.functions import Lower
from django.contrib.auth.models import User
from datetime import datetime, date, time
# from django.utils import timezone


def format_lesson_time(t):
    return t.strftime("%a %d/%m/%Y %H:%M")


def format_confirmation_time(t):
    return t.strftime("%a %d/%m %I:%M %p")


class Confirmation(models.Model):
    teacher = models.ForeignKey(User, related_name="records_confirmations", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_new = models.BooleanField(default=True)

    class Meta:
        ordering = ['teacher', '-id']

    def __str__(self):
        return self.message

    
class Student(models.Model):
    teacher = models.ForeignKey(User, related_name="records_students", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    def nextLesson(self):
        now = datetime.now()
        return self.records_lessons.filter(student=self, start_at__gte=now).first()
    
    class Meta:
        ordering = ['teacher', Lower('name')]
        
    def __str__(self):
        return "{} ({})".format(self.name, self.teacher)

    
class Lesson(models.Model):
    teacher = models.ForeignKey(User, related_name="records_lessons", on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name="records_lessons", on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    duration = models.IntegerField(default=60)
    notes = models.TextField(blank=True)
    notified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Confirmation.objects.create(teacher=self.teacher, message="{}'s {} class saved successfully".format(self.student.name, format_lesson_time(self.start_at)))

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        Confirmation.objects.create(teacher=self.teacher, message="{}'s {} class deleted successfully".format(self.student.name, format_lesson_time(self.start_at)))

        
        
    class Meta:
        ordering = ['teacher', 'start_at']
        
    def __str__(self):
        return "{} {} ({} mins)".format(self.student, format_lesson_time(self.start_at), self.duration)


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

