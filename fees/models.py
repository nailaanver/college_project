from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()


class FeeStructure(models.Model):

    FEE_TYPE_CHOICES = [
        ('TUITION', 'Tuition Fee'),
        ('EXAM', 'Exam Fee'),
        ('SPORTS', 'Sports Fee'),
        ('LIBRARY', 'Library Fine'),
        ('ADMISSION', 'Admission Fee'),
    ]

    COURSE_CHOICES = Student.COURSE_CHOICES
    SEMESTER_CHOICES = Student.SEMESTER_CHOICES

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES,
        null=True,
        blank=True,
        help_text="Leave blank to apply fee to all students"
    )

    fee_type = models.CharField(max_length=50, choices=FEE_TYPE_CHOICES)

    semester = models.PositiveIntegerField(
        choices=SEMESTER_CHOICES,
        null=True,
        blank=True,
        help_text="Leave blank to apply to all semesters"
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)

from library.models import Issue

class Fee(models.Model):

    PAID_BY_CHOICES = [
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('teacher', 'Teacher'),
    ]
    
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="fees"
    )

    # 👇 COMMON FOR STUDENTS & TEACHERS
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="fees",blank=True,null=True
    )

    # 👇 ONLY FOR STUDENT FEES (NULL FOR TEACHER)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    fee_type = models.CharField(max_length=50)

    semester = models.PositiveIntegerField(
        choices=Student.SEMESTER_CHOICES,
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


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TeacherLibraryFine(models.Model):
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True}
    )

    issue = models.OneToOneField(
        "library.Issue",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(max_digits=8, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)
    paid_on = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.username} - ₹{self.amount}"
