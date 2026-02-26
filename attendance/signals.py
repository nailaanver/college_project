from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Count

from .models import Attendance
from notifications.utils import create_notification

User = get_user_model()


@receiver(post_save, sender=Attendance)
def attendance_post_save(sender, instance, created, **kwargs):
    if not created:
        return

    student = instance.student
    student_user = getattr(student, 'user', student)

    # 1️⃣ STUDENT notification (keep same)
    if student_user:
        create_notification(
            recipient=student_user,
            title="Attendance Updated",
            message=f"Your attendance for {instance.subject.name} on {instance.date} is marked as {instance.get_status_display()}",
            notification_type="ATTENDANCE",
            reference_id=instance.id
        )

    # 2️⃣ PARENT notification (keep same)
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

    # 3️⃣ ✅ ADMIN notification — ONLY ON FIRST RECORD
    existing_count = Attendance.objects.filter(
        subject=instance.subject,
        date=instance.date,
        period=instance.period,
        semester=instance.semester
    ).count()

    # If this is the first student attendance for that session
    if existing_count == 1:
        admins = User.objects.filter(is_superuser=True)
        for admin in admins:
            create_notification(
                recipient=admin,
                title="Attendance Marked",
                message=(
                    f"Course: {instance.student.course}\n"
                    f"Semester: {instance.student.semester}\n"
                    f"Period: {instance.period}\n"
                    f"Date: {instance.date}"
                ),
                notification_type="ATTENDANCE",
                reference_id=instance.id
            )