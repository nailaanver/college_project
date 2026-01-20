from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    # Mark all as read
    notifications.filter(is_read=False).update(is_read=True)

    return render(
        request,
        'notifications/notification_list.html',
        {
            'notifications': notifications
        }
    )
