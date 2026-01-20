from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Notification(models.Model):

    NOTIFICATION_TYPES = (
        ('ATTENDANCE', 'Attendance'),
        ('MARKS', 'Internal Marks'),
        ('LIBRARY', 'Library'),
        ('FEES', 'Fees'),
        ('ANNOUNCEMENT', 'Announcement'),
        ('SYSTEM', 'System'),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=200)
    message = models.TextField()

    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # Optional: for linking to related object
    reference_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.recipient} - {self.title}"
