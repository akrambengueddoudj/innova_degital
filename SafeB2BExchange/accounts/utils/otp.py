import random
from django.core.mail import send_mail
from ..models import EmailOTP

def generate_otp(user):
    code = str(random.randint(100000, 999999))
    EmailOTP.objects.create(user=user, code=code)

    send_mail(
        subject="Your OTP Code",
        message=f"Your One-Time Password is: {code}",
        from_email='bengueddoudjakram@gmail.com',
        recipient_list=[user.email],
        fail_silently=False,
    )