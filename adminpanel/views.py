from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from students.models import Student
from teachers.models import Teacher
from students.forms import StudentForm
from teachers.forms import TeacherForm,UserForm
from accounts.models import User
from django.contrib.auth import get_user_model
from teachers.models import Subject
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

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from teachers.forms import UserForm, TeacherForm
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def add_teacher(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST, request.FILES)

        if user_form.is_valid() and teacher_form.is_valid():
            email = user_form.cleaned_data['email']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            dob = teacher_form.cleaned_data['date_of_birth']

            # Check if user already exists
            if User.objects.filter(username=email).exists():
                messages.error(request, "A user with this email already exists.")
            else:
                # Create User
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=dob.strftime('%Y%m%d'),
                    first_name=first_name,
                    last_name=last_name
                )

                # Create Teacher
                teacher = teacher_form.save(commit=False)
                teacher.user = user
                teacher.save()

                messages.success(request, "Teacher added successfully!")
                return redirect('teacher-list')

    else:
        user_form = UserForm()
        teacher_form = TeacherForm()

    return render(request, 'teachers/add_teacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })



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
    
@login_required
@user_passes_test(is_admin)
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student-list')

def add_subject(request):
    if request.method == 'POST':
        name = request.POST['name']
        # code = request.POST['code']
        course = request.POST['course']
        semester = request.POST['semester']
        
        Subject.objects.create(
            name = name,
            # code = code,
            course = course,
            semester = semester
        )
        return redirect('add-subject')
    
    context = {
        'courses':Student.COURSE_CHOICES,
        'semesters':Student.SEMESTER_CHOICES,
            
    }
    return render(request,'adminpanel/add_subject.html',context)

def subject_list(request):
    course = request.GET.get('course', None)
    semester = request.GET.get('semester', None)

    subjects = Subject.objects.all()

    if course:
        subjects = subjects.filter(course=course)
    if semester:
        subjects = subjects.filter(semester=semester)

    context = {
        'subjects': subjects,
        'courses': Student.COURSE_CHOICES,
        'semesters': Student.SEMESTER_CHOICES,
        'selected_course': course,
        'selected_semester': semester,
    }
    return render(request, 'adminpanel/subject_list.html', context)

from django.contrib.admin.views.decorators import staff_member_required
from attendance.models import Attendance

@staff_member_required
def admin_attendance_history(request):

    course = request.GET.get('course')
    semester = request.GET.get('semester')
    period = request.GET.get('period')
    date = request.GET.get('date')

    attendance = Attendance.objects.all()

    if course:
        attendance = attendance.filter(student__course=course)

    if semester:
        attendance = attendance.filter(student__semester=semester)

    if period:
        attendance = attendance.filter(period=period)

    if date:
        attendance = attendance.filter(date=date)

    context = {
        'attendance': attendance,
        'course': course,
        'semester': semester,
        'period': period,
        'date': date,
    }

    return render(
        request,
        'adminpanel/attendance_history.html',
        context
    )
    
from students.models import Student

def course_list(request):
    courses = Student.COURSE_CHOICES
    return render(request, 'courses/course_list.html', {
        'courses': courses
    })

def course_detail(request, course):
    students = Student.objects.filter(course=course).order_by('semester')

    return render(request, 'courses/course_detail.html', {
        'students': students,
        'course_code': course,
        'course_name': dict(Student.COURSE_CHOICES).get(course)
    })
