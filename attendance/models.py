from django.db import models
from students.models import Student
from teachers.models import Subject

from django.utils import timezone


ATTENDANCE_STATUS = [
    ('P', 'Present'),
    ('A', 'Absent'),
    ('L', 'Late'),
]

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    period = models.PositiveIntegerField()  # 1 to 7
    status = models.CharField(max_length=1, choices=ATTENDANCE_STATUS)
    semester = models.PositiveIntegerField(blank=True,null=True)

    class Meta:
        unique_together = ('student', 'subject', 'date', 'period')
