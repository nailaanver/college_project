from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from students.models import Student
from teachers.models import Teacher
from students.forms import StudentForm
from teachers.forms import TeacherForm
from accounts.models import User
from django.contrib.auth import get_user_model
User = get_user_model()



def is_admin(user):
    return user.is_superuser

from django.utils import timezone
from datetime import timedelta

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()

    total_parents = User.objects.filter(
        role='parent',
        parent_student__isnull=False
    ).distinct().count()
    # total_cources = Course.objects.count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        # 'total_cources' : total_cources,
    }

    return render(request, 'adminpanel/admin_dashboard.html', context)




@login_required
def student_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    students = Student.objects.all()
    return render (request,'adminpanel/student_list.html',{'students':students})
                  
# adminpanel/views.py


@login_required
def add_student(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            dob = form.cleaned_data['date_of_birth']
            reg_no = form.cleaned_data['register_number']

            # STUDENT USER
            student_user = User.objects.create_user(
                username=email,
                email=email,
                password=dob.strftime('%Y%m%d'),
                role='student'
            )

            student = form.save(commit=False)
            student.user = student_user
            student.save()

            # create parent user
            parent_user = User.objects.create_user(
                username=f"{reg_no}_parent",
                password=reg_no,
                role='parent'
            )

            # link parent to student
            student.parent = parent_user
            student.save()


            return redirect('student-list')

    else:
        form = StudentForm()

    return render(request, 'adminpanel/add_student.html', {'form': form})


@login_required
def edit_student(request,pk):
    if not request.user.is_superuser:
        return redirect('home')
    
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None,instance=student)
    if form.is_valid():
        form.save()
        return redirect('student-list')
    return render(request,'adminpanel/edit_student.html',{'form':form})

@login_required
def delete_student(request,pk):
    if not request.user.is_superuser:
        return redirect('home')
    student = get_object_or_404(Student,pk=pk)
    student.user.delete()
    student.delete()
    
    return redirect('student-list')


# teacher 

@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            dob = form.cleaned_data['date_of_birth']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            user = User.objects.create_user(
                username=email,
                email=email,
                password=dob.strftime('%Y%m%d'),
                first_name=first_name,
                last_name=last_name
            )

            teacher = form.save(commit=False)
            teacher.user = user
            teacher.save()

            return redirect('teacher-list')
    else:
        form = TeacherForm()

    return render(request, 'teachers/add_teacher.html', {'form': form})

@login_required
def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)

    if request.method == 'POST':
        # update User fields
        teacher.user.first_name = request.POST.get('first_name')
        teacher.user.last_name = request.POST.get('last_name')
        teacher.user.save()

        # update Teacher fields
        teacher.email = request.POST.get('email')
        teacher.subject = request.POST.get('subject')
        teacher.save()

        return redirect('teacher-list')

    # 👇 THIS IS WHY OLD DATA WAS NOT SHOWING
    return render(request, 'teachers/edit_teacher.html', {
        'teacher': teacher   # ✅ REQUIRED
    })

@login_required
def teacher_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    teachers = Teacher.objects.all()
    return render(request, 'teachers/teacher_list.html', {
        'teachers': teachers
    })
    
@login_required
def delete_teacher(request, id):
    if not request.user.is_superuser:
        return redirect('home')

    teacher = get_object_or_404(Teacher, id=id)
    teacher.user.delete()  # delete linked user
    teacher.delete()

    return redirect('teacher-list')

@login_required
def parent_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    parents = User.objects.filter(role='parent')
    return render(request, 'adminpanel/parent_list.html', {
        'parents': parents
    })


