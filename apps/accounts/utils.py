import string
import random
from .models import Player
from django.contrib.auth.models import User


def create_username(last_name, first_name):
    username = first_name[:1].lower() + last_name[:3].lower() + str(random.randrange(10000, 100001, 2))
    ''.join(e for e in username if e.isalnum())

    while User.objects.filter(username=username).exists():
        username = first_name[:1].lower() + last_name[:3].lower() + str(random.randrange(10000, 100001, 2))
        ''.join(e for e in username if e.isalnum())

    return username


def lab_key_generator(size=5, chars=string.ascii_lowercase + string.digits):
    lab_key = ''.join(random.choice(chars) for _ in range(size))
    while Player.objects.filter(lab_key=lab_key).exists():
        lab_key = ''.join(random.choice(chars) for _ in range(size))
    return lab_key