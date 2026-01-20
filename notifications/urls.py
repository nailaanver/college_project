from django.urls import path
from .views import notification_list

app_name = 'notifications'   # ⭐ VERY IMPORTANT

urlpatterns = [
    path('', notification_list, name='notification_list'),
]
