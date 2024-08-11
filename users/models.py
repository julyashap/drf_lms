from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='номер', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
