from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from records.models import Student, Lesson, Notification
from django.contrib.auth.decorators import login_required
from unidecode import unidecode


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
        
        return render(request, "classic/studentlist.html",
                      {'activetab': 'students',
                       'students': students,
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
def studentconfirmdelete(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)

    return render(request, "classic/studentconfirmdelete.html",
                  {'studentId': student_id,
                   'studentName': student.name})


@login_required
def studentdelete(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)
    student.delete()
    return redirect("classic:studentlist")

    
@login_required
def lessonlist(request):
    if request.method == "POST":
        lesson_teacher = request.user
        lesson_student = int(request.POST['student'])
        lesson_day = request.POST['day']
        lesson_start = request.POST['start']
        lesson_duration = int(request.POST['duration'])
        lesson_notes = request.POST['notes']

        student = Student.objects.get(id=lesson_student, teacher=request.user)
        day_fmt = "%d/%m/%Y"
        time_fmt = "%I:%M %p"
        
        day_at = datetime.strptime(lesson_day, day_fmt)
        start_at = datetime.strptime(lesson_start, time_fmt)
        end_at = start_at + timedelta(minutes=lesson_duration)

        Lesson.objects.create(teacher=lesson_teacher,
                              student=student,
                              day=day_at,
                              start_time=start_at,
                              end_time=end_at,
                              notes=lesson_notes)
        return redirect("classic:lessonlist")
    
    else:
        now = datetime.now()
        hr = now.hour
        if hr > 12:
            ampm = "PM"
        else:
            ampm = "AM"

        fixedhr = '{}:00 {}'.format(hr, ampm) 
            
        vueLesson = f"""
        lesson: {{
          student: '',
          day: '',
          start: '{fixedhr}',
          end: '',
          notes: '',
        }}
        """

        lessons = Lesson.objects.filter(teacher=request.user)
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
        new_name = request.POST['name']
        new_phone = request.POST['phone']
        new_email = request.POST['email']

        lesson.teacher = new_teacher
        lesson.name = new_name
        lesson.phone = new_phone
        lesson.email = new_email
        lesson.save()
        
        return redirect("classic:lessonlist")
        
    else:        
        vueLesson = f"""
        lesson: {{
          student: '{lesson.student.id}',
          day: '{lesson.day}',
          start: '{lesson.start_time}',
          end: '{lesson.end_time}',
          notes: '{lesson.notes}',
        }}
        """
    
        return render(request, "classic/lessondetail.html",
                      {'activetab': 'lessons',
                       'lessonId': lesson_id,
                       'students': students,
                       'vueLesson': vueLesson})

    
@login_required
def lessonconfirmdelete(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)

    return render(request, "classic/lessonconfirmdelete.html",
                  {'lessonId': lesson_id,
                   'lessonName': lesson.name})


@login_required
def lessondelete(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
    lesson.delete()
    return redirect("classic:lessonlist")
