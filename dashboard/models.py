from django.db import models
from students.models import Student
from teachers.models import Subject, Teacher

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
    period_number = models.PositiveIntegerField(choices=[(i, f"Period {i}") for i in range(1, 8)])
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('course', 'semester', 'day', 'period_number')

    def __str__(self):
        return f"{self.course} Sem {self.semester} - {self.day} P{self.period_number}"
