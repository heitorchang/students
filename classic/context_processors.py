from datetime import datetime, date, time, timedelta
from records.models import Lesson, Notification

def notifications_processor(request):
    """Get notifications for next day's classes or Monday when Friday"""

    now = datetime.now()
    today = date.today()
    weekday = today.weekday()
    if weekday == 4:
        days_diff = 4
    else:
        days_diff = 2

    end_day = today + timedelta(days=days_diff)
    end_datetime = datetime.combine(end_day, time(0, 0))
    
    if request.user.is_authenticated:
        lessons = Lesson.objects.filter(teacher=request.user, notified=False, start_at__gte=now, start_at__lt=end_datetime)

        for lesson in lessons:
            lesson.notified = True
            lesson.save()
            lesson_start_at = datetime.strftime(lesson.start_at, "%a, %b. %d, %I:%M %p")
            Notification.objects.create(teacher=request.user,
                                        message=f"{lesson.student.name}'s class on {lesson_start_at}",
                                        due_at=lesson.start_at)
            
        notifications = Notification.objects.filter(teacher=request.user, is_new=True)
        return {'notifications': notifications}
    return {'notifications': []}
