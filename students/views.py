from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from students.models import Student

def login_View(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        
        password = dob.replace('-','')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request,user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            if user.role == 'student':
                return redirect('student_dashboard')
            if user.role == 'teacher':
                return redirect('teacher_dashboard')
            if user.role =='parent':
                return redirect('parent_dashboard')
        else:
            return render(request,'login.html', {
                'error':'Invalid login details'
            })
        return render(request,'login.html')