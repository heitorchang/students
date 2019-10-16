from datetime import datetime, date, timedelta
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

        Student.objects.create(teacher=student_teacher,
                               name=student_name,
                               phone=student_phone,
                               email=student_email)
        
        return redirect("classic:studentlist")
    
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
        
        return redirect("classic:studentlist")
        
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

    return render(request, "classic/studentclasses.html",
                  {'activetab': 'students',
                   'student': student,
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

    print(new_start_at)
    for lesson in lessons:
        print(lesson.start_at)
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

        lesson.teacher = new_teacher
        lesson.student = student
        lesson.start_at = new_start_at
        lesson.duration = new_duration
        lesson.notes = new_notes
        lesson.save()
        
        return redirect("classic:lessonlist")
        
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
    return redirect("classic:lessonlist")


@login_required
def profile(request):
    return render(request, "classic/profile.html",
                  {'activetab': 'profile',
                   'username': request.user.username})


@login_required
def lessonthismonth(request):
    return render(request, "classic/lessonthismonth.html")
