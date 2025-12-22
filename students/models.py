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

    register_number = models.CharField(
        max_length=20,
        unique=True
    )

    parent_name = models.CharField(
        max_length=100
    )

    date_of_birth = models.DateField()

    course = models.CharField(
        max_length=20,
        choices=COURSE_CHOICES
    )

    def __str__(self):
        return f"{self.register_number} - {self.user.get_full_name()}"
