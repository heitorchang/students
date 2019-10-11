from django.shortcuts import render, redirect
from records.models import Student, Lesson, Notification
from calendar import day_abbr


def studentlist(request):  
    if request.method == "POST":
        student_teacher = request.user
        student_name = request.POST['name']
        student_phone = request.POST['phone']
        student_email = request.POST['email']

        if request.POST['weekday'].strip() == "":
            student_weekday = None
        else:
            student_weekday = int(request.POST['weekday'])

        if request.POST['hour'] == "" or request.POST['minutes'] == "":
            student_time = None
        else:
            student_time = request.POST['hour'] + request.POST['minutes']

        Student.objects.create(teacher=student_teacher,
                               name=student_name,
                               phone=student_phone,
                               email=student_email,
                               lesson_weekday=student_weekday,
                               lesson_time=student_time)
        
        return redirect("classic:studentlist")
    
    else:
        vueStudent = """
        student: {
          name: '',
          phone: '',
          email: '',
          weekday: '',
          time: '',
        }
        """

        students = Student.objects.filter(teacher=request.user)
        return render(request, "classic/studentlist.html",
                      {'activetab': 'students',
                       'students': students,
                       'day_abbr': day_abbr,
                       'vueStudent': vueStudent})


def studentdetail(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)

    if request.method == "POST":
        new_teacher = request.user
        new_name = request.POST['name']
        new_phone = request.POST['phone']
        new_email = request.POST['email']

        if request.POST['weekday'].strip() == "":
            new_weekday = None
        else:
            new_weekday = int(request.POST['weekday'])

        if request.POST['hour'] == "" or request.POST['minutes'] == "":
            new_time = None
        else:
            new_time = request.POST['hour'] + request.POST['minutes']

        student.teacher = new_teacher
        student.name = new_name
        student.phone = new_phone
        student.email = new_email
        student.lesson_weekday = new_weekday
        student.lesson_time = new_time
        student.save()
        
        return redirect("classic:studentlist")
        
    else:        
        if student.lesson_weekday:
            student_weekday = day_abbr[student.lesson_weekday]
        else:
            student_weekday = ''
        
        vueStudent = f"""
        student: {{
          name: '{student.name}',
          phone: '{student.phone}',
          email: '{student.email}',
          weekday: '{student_weekday}',
          time: '{student.lesson_time}',
        }}
        """
    
        return render(request, "classic/studentdetail.html",
                      {'activetab': 'students',
                       'studentId': student_id,
                       'vueStudent': vueStudent})


def lessonlist(request):
    return render(request, "classic/lessonlist.html", {'activetab': 'lessons'})
