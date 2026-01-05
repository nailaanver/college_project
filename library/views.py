from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book, Issue
from .forms import IssueBookForm
from django.contrib.auth.decorators import login_required, user_passes_test

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

                messages.success(request, f"{book.title} issued to {issue.user.username}.")
                return redirect('issue-book')
    else:
        form = IssueBookForm()

    return render(request, 'library/issue_book.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def return_book_list(request):
    issues = Issue.objects.filter(status='ISSUED')
    return render(request, 'library/return_book_list.html', {'issues': issues})



from datetime import date
from django.contrib import messages
from .forms import ReturnBookForm
from .models import Issue

@login_required
@user_passes_test(is_staff)
def return_book(request, issue_id):
    issue = Issue.objects.get(id=issue_id)

    if request.method == 'POST':
        form = ReturnBookForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.status = 'RETURNED'

            # Update available copies
            book = issue.book
            book.available_copies += 1
            book.save()

            # Calculate fine
            if issue.return_date > issue.due_date:
                overdue_days = (issue.return_date - issue.due_date).days
                issue.fine = overdue_days * 5  # ₹5/day fine

            issue.save()
            messages.success(request, f"{book.title} returned successfully.")
            return redirect('return-book-list')
    else:
        form = ReturnBookForm(instance=issue)

    return render(request, 'library/return_book.html', {'form': form, 'issue': issue})




from django.contrib.auth.decorators import login_required

@login_required
def my_library(request):
    # Fetch all books issued to the logged-in user
    issues = Issue.objects.filter(user=request.user).order_by('-issue_date')
    return render(request, 'library/my_library.html', {'issues': issues})



from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def library_reports(request):
    today = timezone.now().date()

    all_issues = Issue.objects.all().order_by('-issue_date')
    issued_books = Issue.objects.filter(status='ISSUED')
    overdue_books = issued_books.filter(due_date__lt=today)
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

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def book_list(request):
    books = Book.objects.all().order_by('title')

    return render(request, 'library/book_list.html', {
        'books': books
    })


