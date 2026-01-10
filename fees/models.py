from django.db import models
from students.models import Student

class FeeStructure(models.Model):
    FEE_TYPE_CHOICES = [
        ('TUITION', 'Tuition Fee'),
        ('EXAM', 'Exam Fee'),
        ('SPORTS', 'Sports Fee'),
        ('LIBRARY', 'Library Fine'),
        ('ADMISSION', 'Admission Fee'),
    ]

    # Use the same course choices as Student
    COURSE_CHOICES = Student.COURSE_CHOICES

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        null=True,
        blank=True,
        help_text="Leave blank to apply fee to all students"
    )
    fee_type = models.CharField(max_length=50, choices=FEE_TYPE_CHOICES)
    semester = models.PositiveIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        if self.course:
            return f"{self.course} - {self.fee_type}"
        return f"All Students - {self.fee_type}"

from django.db import models
from students.models import Student

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type = models.CharField(max_length=50)
    semester = models.PositiveIntegerField(null=True, blank=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    paid_on = models.DateTimeField(null=True, blank=True)  # ✅ ADD THIS

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.register_number} - {self.fee_type}"
