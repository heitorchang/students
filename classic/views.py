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

        if request.POST['time'].strip() == "":
            student_time = None
        else:
            student_time = request.POST['time']

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
                       'vueStudent': vueStudent})


def studentdetail(request, student_id):
    student = Student.objects.get(id=student_id, teacher=request.user)

    vueStudent = f"""
    student: {{
      name: '{student.name}',
      phone: '{student.phone}',
      email: '{student.email}',
      weekday: '{day_abbr[student.lesson_weekday]}',
      time: '{student.lesson_time}',
    }}
    """
    
    return render(request, "classic/studentdetail.html",
                  {'activetab': 'students',
                   'studentId': student_id,
                   'vueStudent': vueStudent})


def lessonlist(request):
    return render(request, "classic/lessonlist.html", {'activetab': 'lessons'})
