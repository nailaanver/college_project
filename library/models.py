from django.db import models
from django.conf import settings  # <-- change here

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200,null=True)
    author = models.CharField(max_length=150,null=True)
    isbn = models.CharField(max_length=20, unique=True,null=True)
    category = models.CharField(max_length=100,null=True)

    total_copies = models.PositiveIntegerField(null=True)
    available_copies = models.PositiveIntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.title} ({self.author})"


class Issue(models.Model):

    STATUS_CHOICES = (
        ('ISSUED', 'Issued'),
        ('RETURNED', 'Returned'),
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE,null= True)
    
    # CHANGE THIS:
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # <-- use this instead of User
        on_delete=models.CASCADE,null=True
    )

    issue_date = models.DateField(auto_now_add=True,null=True)
    due_date = models.DateField(null=True)

    return_date = models.DateField(null=True, blank=True)

    fine = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0,null=True
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ISSUED',null=True
    )

    def __str__(self):
        return f"{self.book.title} → {self.user}"


from students.models import Student

class LibraryEntry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    entry_time = models.DateTimeField(auto_now_add=True)
    exit_time = models.DateTimeField(null=True, blank=True)
    method = models.CharField(
        max_length=10,
        choices=[('FACE', 'Face'), ('MANUAL', 'Manual')],
        default='FACE'
    )

    def __str__(self):
        return f"{self.student.register_number} - {self.entry_time}"
