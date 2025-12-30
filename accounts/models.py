from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('student','Student'),
        ('teacher','Teacher'),
        ('parent','Parent'),
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        blank=True,
        null=True
    )
    student = models.ForeignKey(
        'students.Student',   # adjust app name if needed
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )