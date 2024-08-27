from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='номер', **NULLABLE)
    city = models.CharField(max_length=100, verbose_name='город', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Payment(models.Model):
    WAY_CHOICES = (
        ('cash', 'наличными'),
        ('bank', 'картой'),
    )

    date = models.DateTimeField(verbose_name='дата', **NULLABLE)
    sum = models.IntegerField(verbose_name='сумма', **NULLABLE)
    way = models.CharField(max_length=4, choices=WAY_CHOICES, verbose_name='способ')
    session_id = models.CharField(max_length=255, verbose_name='идентификатор сессии', **NULLABLE)
    link = models.URLField(max_length=400, verbose_name='ссылка на оплату', **NULLABLE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, verbose_name='урок', **NULLABLE)
