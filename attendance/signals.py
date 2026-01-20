from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Attendance
from notifications.utils import create_notification


@receiver(post_save, sender=Attendance)
def attendance_post_save(sender, instance, created, **kwargs):
    """
    Trigger notifications after attendance is marked
    """
    if not created:
        return

    student = instance.student
    user = student.user

    # Optional: notify student attendance marked
    if user:
        create_notification(
            recipient=user,
            title="Attendance Updated",
            message=f"Your attendance for {instance.subject.name} on {instance.date} is marked as {instance.get_status_display()}",
            notification_type="ATTENDANCE",
            reference_id=instance.id
        )
