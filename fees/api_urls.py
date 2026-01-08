from django.urls import path
from .api_views import FeeListAPI, CreatePaypalPaymentAPI, ExecutePaypalPaymentAPI

urlpatterns = [
    path('list/', FeeListAPI.as_view(), name='api_fee_list'),
    path('create/<int:fee_id>/', CreatePaypalPaymentAPI.as_view(), name='api_create_payment'),
    path('execute/<int:fee_id>/', ExecutePaypalPaymentAPI.as_view(), name='api_execute_payment'),
]
