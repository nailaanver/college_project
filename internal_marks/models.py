from django.db import models
from students.models import Student
from teachers.models import Subject
from dashboard.models import TimeTable
from attendance.models import Attendance


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
    semester = models.PositiveIntegerField(blank=True,null=True)
    class Meta:
        unique_together = ('student', 'subject')

    def calculate_attendance_mark(self):
        total_classes = Attendance.objects.filter(
            student=self.student,
            subject=self.subject
        ).count()

        present_classes = Attendance.objects.filter(
            student=self.student,
            subject=self.subject,
            status__in=['P', 'L']  # Late counts as present
        ).count()

        if total_classes == 0:
            return 0

        percentage = (present_classes / total_classes) * 100

        if percentage >= 90:
            return 5
        elif percentage >= 80:
            return 4
        elif percentage >= 70:
            return 3
        elif percentage >= 60:
            return 2
        else:
            return 0



    def save(self, *args, **kwargs):
        self.test1 = int(self.test1 or 0)
        self.test2 = int(self.test2 or 0)
        self.assignment = int(self.assignment or 0)

        # ✅ SUBJECT-WISE attendance mark
        self.attendance_mark = self.calculate_attendance_mark()

        self.total_internal = (
            self.test1 +
            self.test2 +
            self.assignment +
            self.attendance_mark
        )

        super().save(*args, **kwargs)
