from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Issue
from .forms import IssueBookForm
from django.contrib.auth.decorators import login_required, user_passes_test

from notifications.utils import create_notification


# Only staff/admin can issue books
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            book = issue.book

            if book.available_copies < 1:
                messages.error(request, "No copies available to issue.")
            else:
                # Reduce available copies
                book.available_copies -= 1
                book.save()

                issue.status = 'ISSUED'
                issue.save()
                
                # 🔔 Library Notification (ISSUED)
                create_notification(
                    recipient=issue.user,
                    title="📚 Book Issued",
                    message=f"You have borrowed '{book.title}'. Due date: {issue.due_date}.",
                    notification_type="LIBRARY",
                    reference_id=issue.id
)


                messages.success(request, f"{book.title} issued to {issue.user.username}.")
                return redirect('issue-book')
    else:
        form = IssueBookForm()

    return render(request, 'library/issue_book.html', {
    'form': form,
    'today': now().date()
})


@login_required
@user_passes_test(is_staff)
def return_book_list(request):
    issues = Issue.objects.filter(status='ISSUED')
    return render(request, 'library/return_book_list.html', {'issues': issues})



from datetime import date
from django.contrib import messages
from .forms import ReturnBookForm
from .models import Issue
from fees.models import TeacherLibraryFine


@login_required
@user_passes_test(is_staff)
def return_book(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        form = ReturnBookForm(request.POST, instance=issue)
        if form.is_valid():

            issue = form.save(commit=False)
            issue.status = 'RETURNED'

            # ✅ FORCE set return date automatically
            from django.utils import timezone
            issue.return_date = timezone.now().date()

            issue.save()


            # Increase available copies
            book = issue.book
            book.available_copies += 1
            book.save()

            # 🔥 Calculate fine ONLY if overdue
            if issue.return_date and issue.due_date and issue.return_date > issue.due_date:

                overdue_days = (issue.return_date - issue.due_date).days
                fine_amount = overdue_days * 5

                issue.fine = fine_amount
                issue.fine_paid = False

            else:
                issue.fine = 0
                issue.fine_paid = True

            issue.save()

 
            if Student.objects.filter(user=issue.user).exists():

                student = Student.objects.get(user=issue.user)

                Fee.objects.update_or_create(
                    issue=issue,
                    student=student,
                    defaults={
                        "user": issue.user,
                        "fee_type": "LIBRARY",
                        "amount": fine_amount,
                        "due_date": date.today(),
                        "is_paid": False
                    }
                )

                # If teacher
                # elif Teacher.objects.filter(user=issue.user).exists():
                



            messages.success(request, "Book returned successfully.")
            return redirect('return-book-list')

    else:
        form = ReturnBookForm(instance=issue)

    return render(request, 'library/return_book.html', {
        'form': form,
        'issue': issue
    })




from django.contrib.auth.decorators import login_required

# @login_required
# def my_library(request):
#     issues = Issue.objects.filter(user=request.user).order_by('-issue_date')
#     today = now().date()

#     for issue in issues:
#         if issue.status == 'ISSUED' and issue.due_date < today:
#             issue.overdue_days = (today - issue.due_date).days
#             issue.live_fine = issue.overdue_days * 5
#         else:
#             issue.overdue_days = 0
#             issue.live_fine = issue.fine or 0

#     return render(request, 'library/my_library.html', {'issues': issues})




from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test



@login_required
@user_passes_test(is_staff)
def library_reports(request):
    today = timezone.now().date()

    all_issues = Issue.objects.all().order_by('-issue_date')
    issued_books = Issue.objects.filter(status='ISSUED')
    overdue_books = issued_books.filter(due_date__lt=today)
    
    
    for issue in overdue_books:
        create_notification(
            recipient=issue.user,
            title="⚠️ Library Book Overdue",
            message=(
                f"'{issue.book.title}' is overdue. "
                f"Due date was {issue.due_date}. "
                f"Fine: ₹{(today - issue.due_date).days * 5}"
            ),
            notification_type="LIBRARY",
            reference_id=issue.id
        )

    total_fines = Issue.objects.aggregate(Sum('fine'))['fine__sum'] or 0

    context = {
        'all_issues': all_issues,
        'issued_books': issued_books,
        'overdue_books': overdue_books,
        'total_fines': total_fines,
    }
    return render(request, 'library/library_reports.html', context)


from .forms import BookForm
from django.contrib import messages

@login_required
@user_passes_test(is_staff)
def book_add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully")
            return redirect('book-list')
    else:
        form = BookForm()

    return render(request, 'library/book_form.html', {
        'form': form,
        'title': 'Add Book'
    })
@login_required
@user_passes_test(is_staff)
def book_edit(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully")
            return redirect('book-list')
    else:
        form = BookForm(instance=book)

    return render(request, 'library/book_form.html', {
        'form': form,
        'title': 'Edit Book'
    })
@login_required
@user_passes_test(is_staff)
def book_delete(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        book.delete()
        messages.success(request, "Book deleted successfully")
        return redirect('book-list')

    return render(request, 'library/book_confirm_delete.html', {'book': book})

from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book



@login_required
@user_passes_test(is_staff)
def book_list(request):
    books = Book.objects.all().order_by('title')

    return render(request, 'library/book_list.html', {
        'books': books
    })




from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

@login_required
def my_library(request):
    issues = Issue.objects.filter(user=request.user).order_by('-issue_date')
    today = now().date()

    for issue in issues:
        if issue.status == 'ISSUED' and issue.due_date < today:
            issue.overdue_days = (today - issue.due_date).days
            issue.live_fine = issue.overdue_days * 5
        else:
            issue.overdue_days = 0
            issue.live_fine = issue.fine or 0

    return render(request, 'library/my_library.html', {
        'issues': issues
    })



@login_required
def user_book_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)

    return render(request, 'library/user_book_search.html', {
        'books': books,
        'query': query
    })

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render


@login_required
@user_passes_test(is_staff)
def library_menu(request):
    return render(request, 'library/library_menu.html')

from django.http import HttpResponse
from .models import LibraryEntry



from django.http import HttpResponse
from .models import LibraryEntry
from ai_services.face import recognize_face

def library_face_entry(request):
    student = recognize_face()

    if student is None:
        return HttpResponse("Face not recognized", status=400)

    LibraryEntry.objects.create(student=student)
    return HttpResponse("Library entry recorded")

from fees.models import Fee
from django.shortcuts import get_object_or_404

from django.contrib import messages
from students.models import Student

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from library.models import Issue

# @login_required
# def pay_library_fine(request, issue_id):

#     issue = get_object_or_404(
#         Issue,
#         id=issue_id,
#         user=request.user
#     )

#     # If no fine or already paid
#     if issue.fine <= 0:
#         return redirect("teacher-library")

#     if request.method == "POST":
#         issue.fine = 0
#         issue.save()
#         return redirect("teacher-library")

#     return render(request, "library/pay_fine.html", {
#         "issue": issue,
#         "fine_amount": issue.fine
#     })

from fees.models import TeacherLibraryFine

from django.utils.timezone import now

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now

@login_required
def teacher_pay_fine(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, user=request.user)

    # mark fine as paid
    issue.fine_paid = True
    issue.fine = 0
    issue.save()

    return redirect('teacher-library')


@login_required
def student_library(request):

    if not Student.objects.filter(user=request.user).exists():
        return redirect('teacher-dashboard')

    issues = Issue.objects.filter(user=request.user).order_by('-issue_date')
    today = now().date()

    from fees.models import Fee

    for issue in issues:

        # Check if fee record exists
        fee = Fee.objects.filter(issue=issue, fee_type="LIBRARY").first()

        if fee:
            issue.live_fine = fee.amount
            issue.fine_paid = fee.is_paid
        else:
            # If still issued and overdue (not returned yet)
            if issue.status == 'ISSUED' and issue.due_date < today:
                overdue_days = (today - issue.due_date).days
                issue.live_fine = overdue_days * 5
                issue.fine_paid = False
            else:
                issue.live_fine = 0
                issue.fine_paid = False

    return render(request, 'library/student_library.html', {
        'issues': issues
    })
    
    
from teachers.models import Teacher

from django.utils.timezone import now

@login_required
def teacher_library(request):

    if not Teacher.objects.filter(user=request.user).exists():
        return redirect('student-dashboard')

    issues = Issue.objects.filter(user=request.user).order_by('-issue_date')

    today = now().date()

    for issue in issues:

        # If returned → use stored fine
        if issue.status == "RETURNED":
            issue.display_fine = issue.fine

        # If issued and overdue → calculate live fine
        elif issue.status == "ISSUED" and issue.due_date and today > issue.due_date:
            overdue_days = (today - issue.due_date).days
            issue.display_fine = overdue_days * 5

        else:
            issue.display_fine = 0

    return render(request, 'library/teacher_library.html', {
        'issues': issues,
    })
    
from django.urls import reverse
import paypalrestsdk
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Issue


from datetime import date

@login_required
def pay_fine(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, user=request.user)

    fine_amount = issue.fine



    if fine_amount <= 0 or issue.fine_paid:
        return redirect('teacher-library')

    # Save correct fine to DB
    issue.fine = fine_amount
    issue.save()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(
                reverse('execute-teacher-fine', args=[issue.id])
            ),
            "cancel_url": request.build_absolute_uri(
                reverse('teacher-library')
            ),
        },
        "transactions": [{
            "amount": {
                "total": str(fine_amount),
                "currency": "USD"
            },
            "description": f"Library Fine - {issue.book.title}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)

    return redirect('teacher-library')
    
def payment_success(request):
    issue_id = request.GET.get("issue_id")

    issue = Issue.objects.get(id=issue_id)

    issue.fine_paid = True
    issue.fine = 0
    issue.save()

    return redirect('teacher-library')    
def payment_cancel(request):
    return render(request, "library/payment_cancel.html")

from django.urls import reverse

@login_required
def execute_teacher_fine(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id, user=request.user)

    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    if not payment_id or not payer_id:
        return redirect('teacher-library')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):

        issue.fine_paid = True
        issue.paid_amount = issue.fine   # store original fine
        issue.fine = 0                   # optional
        issue.save()

        url = reverse('teacher-library')
        return redirect(f"{url}?payment=success")
    
    
