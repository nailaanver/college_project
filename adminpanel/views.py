from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from students.models import Student
from teachers.models import Teacher
from students.forms import StudentForm
from teachers.forms import TeacherForm
from accounts.models import User



def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'adminpanel/admin_dashboard.html')


@login_required
def student_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    students = Student.objects.all()
    return render (request,'adminpanel/student_list.html',{'students':students})
                  
@login_required
def add_student(request):
    if not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            email = request.POST.get('email')
            dob = form.cleaned_data['date_of_birth']
            password = dob.strftime('%Y%m%d')

            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                role='student'
            )

            student = form.save(commit=False)
            student.user = user
            student.save()

            return redirect('student-list')
    else:
        form = StudentForm()

    # ✅ ALWAYS return response
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

