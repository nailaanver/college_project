from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import FeeStructureForm
from .models import FeeStructure
from students.models import Student
from .utils import generate_fees_for_student  # function we created before
from notifications.models import Notification
from parents.models import ParentNotification

def create_fee_structure(request):
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            fee_struct = form.save()

            if fee_struct.course:
                students = Student.objects.filter(course=fee_struct.course)
            else:
                students = Student.objects.all()

            from .models import Fee

            for student in students:
                fee_exists = Fee.objects.filter(
                    student=student,
                    fee_type=fee_struct.fee_type,
                    semester=fee_struct.semester
                ).exists()

                if not fee_exists:
                    Fee.objects.create(
                        student=student,
                        fee_type=fee_struct.fee_type,
                        semester=fee_struct.semester,
                        amount=fee_struct.amount,
                        due_date='2026-01-31'
                    )

                    # ---- Student notification (ONLY ONCE) ----
                    if student.user:
                        Notification.objects.create(
                            recipient=student.user,
                            title="💰 Fee Payment Deadline",
                            message=(
                                f"{fee_struct.fee_type} fee of ₹{fee_struct.amount} "
                                f"must be paid before 31 Jan 2026."
                            ),
                            notification_type="FEES"
                        )

                    # ---- Parent notification (ONLY ONCE) ----
                    if student.parent:
                        ParentNotification.objects.create(
                            student=student,
                            title="💰 Fee Payment Deadline",
                            message=(
                                f"{student.first_name}'s {fee_struct.fee_type} fee "
                                f"of ₹{fee_struct.amount} is due on 31 Jan 2026."
                            )
                        )

            return redirect('fee_list')
    else:
        form = FeeStructureForm()

    return render(request, 'fees/create_fee.html', {'form': form})



def fee_list(request):
    from .models import Fee
    fees = Fee.objects.all()
    return render(request, 'fees/fee_list.html', {'fees': fees})

