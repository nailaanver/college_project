from django.core.management.base import BaseCommand
from django.utils import timezone
from attendance.models import Attendance
from teachers.models import Teacher
from notifications.utils import create_notification

class Command(BaseCommand):
    help = "Send reminder to teachers who haven't submitted attendance"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        for teacher in Teacher.objects.all():
            subjects = teacher.subjects.all()

            for subject in subjects:
                attendance_exists = Attendance.objects.filter(
                    subject=subject,
                    date=today
                ).exists()

                if not attendance_exists:
                    create_notification(
                        recipient=teacher.user,
                        title="Attendance Pending",
                        message=f"You have not submitted attendance for {subject.name} today.",
                        notification_type="ATTENDANCE"
                    )
