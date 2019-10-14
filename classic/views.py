from django.shortcuts import render, redirect
from records.models import Student, Lesson, Notification
from calendar import day_abbr
from django.contrib.auth.decorators import login_required


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
        return render(request, "classic/studentlist.html",
                      {'activetab': 'students',
                       'students': students,
                       'day_abbr': day_abbr,
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
def lessonlist(request):
    return render(request, "classic/lessonlist.html", {'activetab': 'lessons'})
