import random
from django.core.cache import cache
from celery import shared_task
from rest_framework_simplejwt.tokens import RefreshToken


def generate_verification_code():
    code  = str(random.randint(1000,9999))
    return code, 50


@shared_task
def send_verification_code(phone_number, code):
    print(f"Foydalanuvchiga {phone_number} raqamiga {code} kodi yuborildi.")
    # Haqiqiy SMS xizmati:
    # twilio_client.messages.create(to=phone_number, from_="YOUR_TWILIO_NUMBER", body=f"Sizning tasdiqlash kodingiz: {code}")
    cache.set(f"verification_code_{phone_number}", code, timeout=300)  # 5 daqiqa saqlash

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }