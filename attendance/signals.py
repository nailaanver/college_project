from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Attendance
from notifications.utils import create_notification

User = get_user_model()


@receiver(post_save, sender=Attendance)
def attendance_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    student = instance.student  # may be User or Student

    # 1️⃣ STUDENT notification
    student_user = getattr(student, 'user', student)

    if student_user:
        create_notification(
            recipient=student_user,
            title="Attendance Updated",
            message=f"Your attendance for {instance.subject.name} on {instance.date} is marked as {instance.get_status_display()}",
            notification_type="ATTENDANCE",
            reference_id=instance.id
        )

    # 2️⃣ PARENT notification
    parent = getattr(student, 'parent', None)

    parent_user = getattr(parent, 'user', None)
    if parent_user:
        create_notification(
            recipient=parent_user,
            title="Student Attendance Updated",
            message=f"{student_user.get_full_name()}'s attendance for {instance.subject.name} on {instance.date} is marked as {instance.get_status_display()}",
            notification_type="ATTENDANCE",
            reference_id=instance.id
        )

    # 3️⃣ ADMIN notification
    admins = User.objects.filter(is_superuser=True)
    for admin in admins:
        create_notification(
            recipient=admin,
            title="Attendance Marked",
            message=f"Course: {instance.student.course}\nSemester: {instance.student.semester}\nPeriod: {instance.period}\nDate: {instance.date}",
            notification_type="ATTENDANCE",
            reference_id=instance.id
        )
