from datetime import datetime, date, time, timedelta
from records.models import Lesson, Notification, Confirmation

def notifications_processor(request):
    """Get notifications for next day's classes or Monday when Friday"""

    now = datetime.now()
    today = date.today()

    # DISABLED--seems confusing to have different behavior
    # On Fridays, get notified for the weekend and next Monday
    #
    # weekday = today.weekday()
    # if weekday == 4:
    #     days_diff = 4
    # else:

    # Get notified for classes on the next day
    days_diff = 2

    end_day = today + timedelta(days=days_diff)
    end_datetime = datetime.combine(end_day, time(0, 0))
    
    if request.user.is_authenticated:
        lessons = Lesson.objects.filter(teacher=request.user, notified=False, start_at__gte=now, start_at__lt=end_datetime)

        # Combine all classes into one message
        messages = ""

        for lesson in lessons:
            lesson.notified = True
            lesson.save()
            lesson_start_at = datetime.strftime(lesson.start_at, "%a, %b. %d, %I:%M %p")
            messages += f"{lesson.student.name}'s class on {lesson_start_at}<br>"

        if messages != "":
            Notification.objects.create(teacher=request.user,
                                        message=messages,
                                        due_at=end_datetime)
            
        notifications = Notification.objects.filter(teacher=request.user, is_new=True)
        confirmations = Confirmation.objects.filter(teacher=request.user, is_new=True)

        for c in confirmations:
            c.is_new = False
            c.save()

        confirmations = confirmations[:1]
        
        return {'notifications': notifications,
                'confirmations': confirmations}
    
    return {'notifications': [],
            'confirmations': []}
