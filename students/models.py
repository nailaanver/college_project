from django.db import models
from accounts.models import User

class Student(models.Model):

    COURSE_CHOICES = (
        ('BCA', 'BCA'),
        ('BSC_CS', 'BSc Computer Science'),
        ('BSC_IT', 'BSc Information Technology'),
        ('BCOM', 'BCom'),
        ('BA', 'BA'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50,blank=True)   # Student first name
    last_name = models.CharField(max_length=50,blank=True)    # Student last name

    father_name = models.CharField(max_length=100,blank=True)
    mother_name = models.CharField(max_length=100,blank=True)

    register_number = models.CharField(
        max_length=20,
        unique=True
    )

    date_of_birth = models.DateField()

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES
    )

    profile_photo = models.ImageField(
        upload_to='student_profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.register_number} - {self.first_name} {self.last_name}"
