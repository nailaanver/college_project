from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class Teacher(models.Model):
    SUBJECT_CHOICES = (
        ('MATHS', 'Mathematics'),
        ('PHY', 'Physics'),
        ('CHEM', 'Chemistry'),
        ('CS', 'Computer Science'),
        ('ENG', 'English'),
        ('ML','Malayalam'),
        ('CM','Commerce'),
        ('FN','Financial')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, null=True)
    profile_photo = models.ImageField(upload_to='teachers/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.email

class Subject(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=20, choices=Student.COURSE_CHOICES)
    semester = models.PositiveIntegerField(choices=Student.SEMESTER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.course} Sem {self.semester})"
