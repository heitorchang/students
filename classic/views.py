from datetime import datetime, date, time, timedelta
from calendar import monthrange, month_name
from collections import defaultdict, namedtuple
from operator import itemgetter
from django.shortcuts import render, redirect
from records.models import Student, Lesson, Notification
from django.contrib.auth.decorators import login_required
from unidecode import unidecode
# from django.utils import timezone


@login_required
def studentlist(request):  
    if request.method == "POST":
        student_teacher = request.user
        student_name = request.POST['name']
        student_phone = request.POST['phone']
        student_email = request.POST['email']

        createdStudent = Student.objects.create(teacher=student_teacher,
                                                name=student_name,
                                                phone=student_phone,
                                                email=student_email)
        
        return redirect("classic:studentclasses", createdStudent.id)
    
    else:
        vueStudent = """
        student: {
          name: '',
          phone: '',
          email: '',
        }
        """

        students = Student.objects.filter(teacher=request.user)
        students = sorted(students, key=lambda s: unidecode(s.name.lower()))

        page_loaded = datetime.now()
        
        return render(request, "classic/studentlist.html",
                      {'activetab': 'students',
                       'students': students,
                       'page_loaded': page_loaded,
                       'vueStudent': vueStudent})


@login_required
def studentdetail(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)

    if request.method == "POST":
        new_teacher = request.user
        new_name = request.POST['name']
        new_phone = request.POST['phone']
        new_email = request.POST['email']

        student.teacher = new_teacher
        student.name = new_name
        student.phone = new_phone
        student.email = new_email
        student.save()
        
        return redirect("classic:studentclasses", student_id)
        
    else:        
        vueStudent = f"""
        student: {{
          name: '{student.name}',
          phone: '{student.phone}',
          email: '{student.email}',
        }}
        """
    
        return render(request, "classic/studentdetail.html",
                      {'activetab': 'students',
                       'studentId': student_id,
                       'vueStudent': vueStudent})

    
@login_required
def studentclasses(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)
    upcomingclasses = Lesson.objects.filter(student=student, start_at__gte=datetime.now())

    # generate links for class history (months with at least one class)
    lessons = Lesson.objects.filter(teacher=request.user,
                                    student=student)

    monthlinks_set = set()
    for lesson in lessons:
        year = lesson.start_at.year
        month = lesson.start_at.month
        monthname = month_name[month]
        monthlinks_set.add((year, month, monthname))

    return render(request, "classic/studentclasses.html",
                  {'activetab': 'students',
                   'student': student,
                   'monthlinks': sorted(monthlinks_set),
                   'upcomingclasses': upcomingclasses})


@login_required
def studentconfirmdelete(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)

    return render(request, "classic/studentconfirmdelete.html",
                  {'activetab': 'students',
                   'studentId': student_id,
                   'studentName': student.name})


@login_required
def studentdelete(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)
    student.delete()
    return redirect("classic:studentlist")


def lessonConflicts(request, new_start_at):
    """Return True if newLesson starts in another lesson's time window"""
    lessons = Lesson.objects.filter(teacher=request.user)

    for lesson in lessons:
        if lesson.start_at <= new_start_at < lesson.start_at + timedelta(minutes=lesson.duration):
            return lesson
    return None


def editLessonConflicts(request, editedLesson, new_start_at):
    """Return True if newLesson starts in another lesson's time window"""
    lessons = Lesson.objects.filter(teacher=request.user)
    
    for lesson in lessons:
        if lesson.id != editedLesson.id:
            if lesson.start_at <= new_start_at < lesson.start_at + timedelta(minutes=lesson.duration):
                return lesson
    return None


@login_required
def lessonall(request):
    lessons = Lesson.objects.filter(teacher=request.user)
    return render(request, "classic/lessonall.html",
                  {'activetab': 'lessons',
                   'lessons': lessons})

    
@login_required
def lessonlist(request):
    if request.method == "POST":
        lesson_teacher = request.user
        lesson_student = int(request.POST['student'])
        lesson_day = request.POST['day']
        lesson_start = request.POST['start']
        lesson_duration = int(request.POST['duration'])
        lesson_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=lesson_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        start_at = datetime.strptime(lesson_day + " " + lesson_start, start_at_fmt)

        conflictingLesson = lessonConflicts(request, start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': start_at})
        
        Lesson.objects.create(teacher=lesson_teacher,
                              student=student,
                              start_at=start_at,
                              duration=lesson_duration,
                              notes=lesson_notes)
        return redirect("classic:lessonlist")
    
    else:
        vueLesson = f"""
        lesson: {{
          student: '',
          day: '',
          start: '',
          duration: '60',
          notes: ``,
        }}
        """

        lessons = Lesson.objects.filter(teacher=request.user, start_at__gte=datetime.now())
        students = Student.objects.filter(teacher=request.user)
        students = sorted(students, key=lambda s: unidecode(s.name.lower()))

        return render(request, "classic/lessonlist.html",
                      {'activetab': 'lessons',
                       'hasModal': True,
                       'lessons': lessons,
                       'students': students,
                       'vueLesson': vueLesson})


@login_required
def lessondetail(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
    students = Student.objects.filter(teacher=request.user)
    students = sorted(students, key=lambda s: unidecode(s.name.lower()))

    if request.method == "POST":
        new_teacher = request.user
        new_student = int(request.POST['student'])
        new_day = request.POST['day']
        new_start = request.POST['start']
        new_duration = int(request.POST['duration'])
        new_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=new_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        new_start_at = datetime.strptime(new_day + " " + new_start, start_at_fmt)

        conflictingLesson = editLessonConflicts(request, lesson, new_start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': new_start_at})

        lesson.teacher = new_teacher
        lesson.student = student
        lesson.start_at = new_start_at
        lesson.duration = new_duration
        lesson.notes = new_notes

        # Reset notified because a postponed class needs a new notification
        lesson.notified = False
        lesson.save()
        
        return redirect("classic:calendarthismonth")
        
    else:
        lesson_day = datetime.strftime(lesson.start_at, "%Y-%m-%d")
        lesson_start_time = datetime.strftime(lesson.start_at, "%H:%M")
        
        vueLesson = f"""
        lesson: {{
          student: '{lesson.student.id}',
          day: '{lesson_day}',
          start: '{lesson_start_time}',
          duration: '{lesson.duration}',
          notes: `{lesson.notes}`,
        }}
        """
    
        return render(request, "classic/lessondetail.html",
                      {'activetab': 'lessons',
                       'lessonId': lesson_id,
                       'students': students,
                       'vueLesson': vueLesson})


@login_required
def lessoncard(request, lesson_id):
    if request.method == "POST":
        lesson_teacher = request.user
        lesson_student = int(request.POST['student'])
        lesson_day = request.POST['day']
        lesson_start = request.POST['start']
        lesson_duration = int(request.POST['duration'])
        lesson_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=lesson_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        start_at = datetime.strptime(lesson_day + " " + lesson_start, start_at_fmt)

        conflictingLesson = lessonConflicts(request, start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': start_at})

        Lesson.objects.create(teacher=lesson_teacher,
                              student=student,
                              start_at=start_at,
                              duration=lesson_duration,
                              notes=lesson_notes)
        return redirect("classic:studentclasses", student.id)
    
    else:
        lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
        students = Student.objects.filter(teacher=request.user)
        students = sorted(students, key=lambda s: unidecode(s.name.lower()))

        nextWeek = datetime.strftime(lesson.start_at + timedelta(days=7), "%Y-%m-%d")
        startTime = datetime.strftime(lesson.start_at, "%H:%M")
        
        vueLesson = f"""
        lesson: {{
          student: '{lesson.student.id}',
          day: '{nextWeek}',
          start: '{startTime}',
          duration: '{lesson.duration}',
          notes: ``,
        }}
        """

        return render(request, "classic/lessoncard.html",
                      {'activetab': 'lessons',
                       'lesson': lesson,
                       'students': students,
                       'vueLesson': vueLesson})
    

@login_required
def lessonforstudent(request, student_id):
    students = Student.objects.filter(teacher=request.user)
    students = sorted(students, key=lambda s: unidecode(s.name.lower()))

    if request.method == "POST":
        new_teacher = request.user
        new_student = int(request.POST['student'])
        new_day = request.POST['day']
        new_start = request.POST['start']
        new_duration = int(request.POST['duration'])
        new_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=new_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        new_start_at = datetime.strptime(new_day + " " + new_start, start_at_fmt)

        conflictingLesson = lessonConflicts(request, new_start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': new_start_at})

        Lesson.objects.create(teacher=new_teacher,
                              student=student,
                              start_at=new_start_at,
                              duration = new_duration,
                              notes=new_notes)
        
        return redirect("classic:studentclasses", student_id)
        
    else:
        vueLesson = f"""
        lesson: {{
          student: '{student_id}',
          day: '',
          start: '',
          duration: '60',
          notes: ``,
        }}
        """
    
        return render(request, "classic/lessonforstudent.html",
                      {'activetab': 'lessons',
                       'students': students,
                       'vueLesson': vueLesson})

    
@login_required
def lessonadd(request, prefilled_date=""):
    if request.method == "POST":
        lesson_teacher = request.user
        lesson_student = int(request.POST['student'])
        lesson_day = request.POST['day']
        lesson_start = request.POST['start']
        lesson_duration = int(request.POST['duration'])
        lesson_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=lesson_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        start_at = datetime.strptime(lesson_day + " " + lesson_start, start_at_fmt)

        conflictingLesson = lessonConflicts(request, start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': start_at})
        
        createdLesson = Lesson.objects.create(teacher=lesson_teacher,
                                              student=student,
                                              start_at=start_at,
                                              duration=lesson_duration,
                                              notes=lesson_notes)
        return redirect("classic:calendarmonth", start_at.year, start_at.month)
    
    else:
        vueLesson = f"""
        lesson: {{
          student: '',
          day: '{prefilled_date}',
          start: '',
          duration: '60',
          notes: ``,
        }}
        """

        lessons = Lesson.objects.filter(teacher=request.user, start_at__gte=datetime.now())
        students = Student.objects.filter(teacher=request.user)
        students = sorted(students, key=lambda s: unidecode(s.name.lower()))

        return render(request, "classic/lessonadd.html",
                      {'activetab': 'lessons',
                       'lessons': lessons,
                       'students': students,
                       'vueLesson': vueLesson})


@login_required
def lessonconfirmdelete(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)

    return render(request, "classic/lessonconfirmdelete.html",
                  {'activetab': 'lessons',
                   'lessonId': lesson_id,
                   'lesson': lesson})


@login_required
def lessondelete(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
    lesson.delete()
    return redirect("classic:calendarthismonth")


@login_required
def profile(request):
    upcoming_lesssons = Lesson.objects.filter(teacher=request.user, start_at__gte=datetime.now(), start_at__lte=datetime.now() + timedelta(days=15))
    
    return render(request, "classic/profile.html",
                  {'activetab': 'profile',
                   'lessons': upcoming_lesssons,
                   'username': request.user.username})


@login_required
def lessonthismonth(request):
    return render(request, "classic/lessonthismonth.html")


# Calendar views

def monthlyreport(request, year, month):
    startlessons = datetime(year, month, 1, 0, 0, 0)
    endlessons = datetime(year, month, monthrange(year, month)[1], 23, 59, 59)
    
    lessons = Lesson.objects.filter(teacher=request.user, start_at__gte=startlessons, start_at__lte=endlessons)

    now = datetime.now()

    totalcompleted = 0
    totalupcoming = 0
    totaltotal = 0

    studentdict = {student.id: {"name": student.name,
                                "id": student.id,
                                "completed": 0,
                                "upcoming": 0,
                                "total": 0}
                   for student in Student.objects.filter(teacher=request.user)}
    
    for lesson in lessons:
        studentdict[lesson.student.id]['total'] += 1
        totaltotal += 1
        if lesson.start_at <= now:
            studentdict[lesson.student.id]['completed'] += 1
            totalcompleted += 1
        else:
            studentdict[lesson.student.id]['upcoming'] += 1
            totalupcoming += 1

    filtered = sorted((v for (k, v) in studentdict.items() if (v['completed'] + v['upcoming']) > 0), key=itemgetter('name'))

    filtered.append({"name": "Total",
                     "id": -1,
                     "completed": totalcompleted,
                     "upcoming": totalupcoming,
                     "total": totaltotal})
    
    return filtered


@login_required
def calendarmonth(request, year, month):
    if request.method == "POST":
        lesson_teacher = request.user
        lesson_student = int(request.POST['student'])
        lesson_day = request.POST['day']
        lesson_start = request.POST['start']
        lesson_duration = int(request.POST['duration'])
        lesson_notes = request.POST['notes'].strip()

        student = Student.objects.get(id=lesson_student, teacher=request.user)
        start_at_fmt = "%Y-%m-%d %H:%M"
        
        start_at = datetime.strptime(lesson_day + " " + lesson_start, start_at_fmt)

        conflictingLesson = lessonConflicts(request, start_at)

        if conflictingLesson:
            return render(request, "classic/lessonconflict.html",
                          {'conflictingLesson': conflictingLesson,
                           'newStartAt': start_at})
        
        Lesson.objects.create(teacher=lesson_teacher,
                              student=student,
                              start_at=start_at,
                              duration=lesson_duration,
                              notes=lesson_notes)
        return redirect("classic:calendarmonth", year, month)

    else:
        vueLesson = f"""
        lesson: {{
          student: '',
          day: '',
          start: '',
          duration: '60',
          notes: ``,
        }}
        """

        weekslist = []
        first = date(year, month, 1)
        last = date(year, month, monthrange(year, month)[1])

        # Count extra days to the first and last weeks. These will belong
        # to other months
        firstextras = (first.weekday() + 1) % 7
        lastextras = 6 - ((last.weekday() + 1) % 7)

        firstcalday = first - timedelta(days=firstextras)
        lastcalday = last + timedelta(days=lastextras)

        days = (lastcalday - firstcalday).days + 1
        weeks = days // 7

        assert firstcalday.weekday() == 6
        assert lastcalday.weekday() == 5

        startlessons = datetime.combine(firstcalday, time(0, 0, 0))
        endlessons = datetime.combine(lastcalday, time(23, 59, 59))
        lessons = Lesson.objects.filter(teacher=request.user, start_at__gte=startlessons, start_at__lte=endlessons)
        lessonsdict = defaultdict(list)

        for lesson in lessons:
            lessonsdict[datetime.strftime(lesson.start_at.date(), "%Y-%m-%d")].append(lesson)

        for i in range(weeks):
            week = []
            for d in range(7):
                daylabel = datetime.strftime(firstcalday, "%d")
                if daylabel[0] == "0":
                    daylabel = daylabel[1]
                week.append({'longlabel': datetime.strftime(firstcalday, "%a, %b. %d, %I:%M %p"),
                             'label': daylabel,
                             'ymd': datetime.strftime(firstcalday, "%Y-%m-%d"),
                             'modalLabel': datetime.strftime(firstcalday, "%a, %b. %d"),
                             'modalId': "id" + datetime.strftime(firstcalday, "%Y-%m-%d"),
                             'lessons': lessonsdict[datetime.strftime(firstcalday, "%Y-%m-%d")],})
                firstcalday += timedelta(days=1)
            weekslist.append(week[:])
            
        students = Student.objects.filter(teacher=request.user)
        students = sorted(students, key=lambda s: unidecode(s.name.lower()))

        headermonth = datetime.strftime(date(year, month, 1), "%B %Y")
        headermonthshort = datetime.strftime(date(year, month, 1), "%b %Y")

        if month == 1:
            prevMonth = 12
            prevYear = year - 1
        else:
            prevMonth = month - 1
            prevYear = year

        if month == 12:
            nextMonth = 1
            nextYear = year + 1
        else:
            nextMonth = month + 1
            nextYear = year

        # monthly report
        studentreport = monthlyreport(request, year, month)
        page_loaded = datetime.now()

        return render(request, "classic/calendarmonth.html",
                      {'activetab': 'lessons',
                       'lessons': lessons,
                       'students': students,
                       'headermonth': headermonth,
                       'headermonthshort': headermonthshort,
                       'weeks': weekslist,
                       'prevMonth': prevMonth,
                       'prevYear': prevYear,
                       'nextMonth': nextMonth,
                       'nextYear': nextYear,
                       'hasModal': True,
                       'todayymd': date.today().strftime("%Y-%m-%d"),
                       'studentreport': studentreport,
                       'page_loaded': page_loaded,
                       'vueLesson': vueLesson})
    

@login_required
def calendarthismonth(request):
    today = date.today()
    return calendarmonth(request, today.year, today.month)


@login_required
def studentadd(request):
    if request.method == "POST":
        student_teacher = request.user
        student_name = request.POST['name']
        student_phone = request.POST['phone']
        student_email = request.POST['email']

        createdStudent = Student.objects.create(teacher=student_teacher,
                                                name=student_name,
                                                phone=student_phone,
                                                email=student_email)
        
        return redirect("classic:studentclasses", createdStudent.id)
    
    else:
        vueStudent = """
        student: {
          name: '',
          phone: '',
          email: '',
        }
        """

    return render(request, "classic/studentadd.html",
                  {'activetab': 'students',
                   'vueStudent': vueStudent})


@login_required
def studentmonth(request, student_id, year, month):
    student = Student.objects.get(teacher=request.user, id=student_id)
    lessons = Lesson.objects.filter(teacher=request.user,
                                    student=student,
                                    start_at__gte=datetime(year, month, 1, 0, 0, 0),
                                    start_at__lte=datetime(year, month, monthrange(year, month)[1], 23, 59, 59))

    headermonth = datetime.strftime(date(year, month, 1), "%B %Y")

    # generate links for class history (months with at least one class)
    all_lessons = Lesson.objects.filter(teacher=request.user,
                                        student=student)
    monthlinks_set = set()
    for lesson in all_lessons:
        year = lesson.start_at.year
        month = lesson.start_at.month
        monthname = month_name[month]
        monthlinks_set.add((year, month, monthname))

    return render(request, "classic/studentmonth.html",
                  {'activetab': 'students',
                   'student': student,
                   'headermonth': headermonth,
                   'year': year,
                   'month': month,
                   'monthlinks': sorted(monthlinks_set),
                   'lessons': lessons})
    
