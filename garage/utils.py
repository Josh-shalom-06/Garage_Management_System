from twilio.rest import Client
from django.conf import settings

def send_sms(to, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    
    try:
        client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        return True
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False
