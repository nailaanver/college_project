from django.db import models
from students.models import Student
from teachers.models import Subject

class TimeTable(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    course = models.CharField(max_length=20, choices=Student.COURSE_CHOICES)
    semester = models.PositiveIntegerField(choices=Student.SEMESTER_CHOICES)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    period_number = models.PositiveIntegerField()  # 1 to 7
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'semester', 'day', 'period_number')
