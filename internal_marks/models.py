from django.db import models
from students.models import Student
from teachers.models import Subject
from dashboard.models import TimeTable

class InternalMark(models.Model):

    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    timetable = models.ForeignKey(
        TimeTable,
        on_delete=models.CASCADE
    )

    test1 = models.PositiveIntegerField(default=0)
    test2 = models.PositiveIntegerField(default=0)
    assignment = models.PositiveIntegerField(default=0)

    attendance_mark = models.PositiveIntegerField(default=0)
    total_internal = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Draft'
    )

    class Meta:
        unique_together = ('student', 'subject')

    def save(self, *args, **kwargs):
        self.test1 = int(self.test1 or 0)
        self.test2 = int(self.test2 or 0)
        self.assignment = int(self.assignment or 0)
        self.attendance_mark = int(self.attendance_mark or 0)

        self.total_internal = (
            self.test1 +
            self.test2 +
            self.assignment +
            self.attendance_mark
        )
        super().save(*args, **kwargs)

