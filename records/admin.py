from django.contrib import admin
from . import models

admin.site.register(models.Student)
admin.site.register(models.Lesson)
admin.site.register(models.Notification)
admin.site.register(models.Confirmation)
