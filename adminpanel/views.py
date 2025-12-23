from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render,redirect,get_object_or_404
from students.models import Student
from students.forms import StudentForm
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