from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Notification


def notification_list(request):

    # -------------------------------------------------
    # AUTH CHECK (PARENT + OTHERS)
    # -------------------------------------------------
    if not request.user.is_authenticated:
        return redirect('role_login')

    # -------------------------------------------------
    # FETCH NOTIFICATIONS (WORKS FOR ALL ROLES)
    # -------------------------------------------------
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    notifications.filter(is_read=False).update(is_read=True)

    # -------------------------------------------------
    # DASHBOARD ROUTING
    # -------------------------------------------------
    if request.user.is_superuser:
        dashboard_url = reverse('admin-dashboard')

    elif hasattr(request.user, 'teacher'):
        dashboard_url = reverse('teacher-dashboard')

    elif hasattr(request.user, 'parent'):
        dashboard_url = reverse('parent-dashboard')

    else:
        dashboard_url = reverse('student-dashboard')

    return render(
        request,
        'notifications/notification_list.html',
        {
            'notifications': notifications,
            'dashboard_url': dashboard_url
        }
    )
