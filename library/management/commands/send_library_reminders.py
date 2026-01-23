from django.core.management.base import BaseCommand
from django.utils.timezone import now
from datetime import timedelta

from library.models import Issue
from notifications.utils import create_notification


class Command(BaseCommand):
    help = "Send library due-date reminders and overdue notifications"

    def handle(self, *args, **kwargs):
        today = now().date()
        tomorrow = today + timedelta(days=1)

        # 🔔 1-day reminder
        issues_due_tomorrow = Issue.objects.filter(
            status='ISSUED',
            due_date=tomorrow,
            reminder_sent=False
        )

        for issue in issues_due_tomorrow:
            # Student
            create_notification(
                recipient=issue.user,
                title="⏰ Library Due Date Reminder",
                message=f"'{issue.book.title}' is due tomorrow ({issue.due_date}).",
                notification_type="LIBRARY",
                reference_id=issue.id
            )

            # Teacher (if exists)
            if hasattr(issue.user, 'teacher'):
                create_notification(
                    recipient=issue.user,
                    title="⏰ Library Due Date Reminder",
                    message=f"'{issue.book.title}' is due tomorrow.",
                    notification_type="LIBRARY",
                    reference_id=issue.id
                )

            issue.reminder_sent = True
            issue.save()

        # ⚠️ Overdue
        overdue_issues = Issue.objects.filter(
            status='ISSUED',
            due_date__lt=today,
            overdue_notified=False
        )

        for issue in overdue_issues:
            days = (today - issue.due_date).days

            create_notification(
                recipient=issue.user,
                title="⚠️ Library Book Overdue",
                message=f"'{issue.book.title}' is overdue by {days} day(s).",
                notification_type="LIBRARY",
                reference_id=issue.id
            )

            issue.overdue_notified = True
            issue.save()

        self.stdout.write(self.style.SUCCESS("Library reminders processed"))
