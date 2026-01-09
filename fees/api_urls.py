from django.urls import path
from . import api_views
urlpatterns = [
    path('create/<int:fee_id>/', api_views.create_paypal_payment, name='api_create_payment'),
    path('execute/<int:fee_id>/', api_views.execute_paypal_payment, name='api_execute_payment'),
]

