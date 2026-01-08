import paypalrestsdk
from django.conf import settings

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox for testing, live for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET
})
