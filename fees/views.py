from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import FeeStructureForm
from .models import FeeStructure
from students.models import Student
from .utils import generate_fees_for_student  # function we created before

def create_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            fee_struct = form.save()
            
            # Assign fees to relevant students immediately
            if fee_struct.course:
                students = Student.objects.filter(course=fee_struct.course)
            else:
                students = Student.objects.all()
            
            for student in students:
                # Avoid duplicates
                from .models import Fee
                if not Fee.objects.filter(
                    student=student, 
                    fee_type=fee_struct.fee_type, 
                    semester=fee_struct.semester
                ).exists():
                    Fee.objects.create(
                        student=student,
                        fee_type=fee_struct.fee_type,
                        semester=fee_struct.semester,
                        amount=fee_struct.amount,
                        due_date='2026-01-31'  # set default due date
                    )
            
            return redirect('fee_list')  # redirect to fee list page
    else:
        form = FeeStructureForm()
    
    return render(request, 'fees/create_fee.html', {'form': form})


def fee_list(request):
    from .models import Fee
    fees = Fee.objects.all()
    return render(request, 'fees/fee_list.html', {'fees': fees})

