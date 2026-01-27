from django.db import models
from students.models import Student

from students.models import Student

class FeeStructure(models.Model):

    FEE_TYPE_CHOICES = [
        ('TUITION', 'Tuition Fee'),
        ('EXAM', 'Exam Fee'),
        ('SPORTS', 'Sports Fee'),
        ('LIBRARY', 'Library Fine'),
        ('ADMISSION', 'Admission Fee'),
    ]

    COURSE_CHOICES = Student.COURSE_CHOICES
    SEMESTER_CHOICES = Student.SEMESTER_CHOICES  # 👈 reuse

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        null=True,
        blank=True,
        help_text="Leave blank to apply fee to all students"
    )

    fee_type = models.CharField(max_length=50, choices=FEE_TYPE_CHOICES)

    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES,   # ✅ DROPDOWN
        null=True,
        blank=True,
        help_text="Leave blank to apply to all semesters"
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    
class Fee(models.Model):

    PAID_BY_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
    ]

    SEMESTER_CHOICES = Student.SEMESTER_CHOICES  # 👈 reuse

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=50)

    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES,   # ✅ DROPDOWN
        null=True,
        blank=True
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)

    paid_by = models.CharField(
        max_length=10,
        choices=PAID_BY_CHOICES,
        null=True,
        blank=True
    )

    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    paid_on = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

