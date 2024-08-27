from django.db import models

from config import settings

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    price = models.IntegerField(verbose_name='цена', **NULLABLE)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')
    preview = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    video = models.URLField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)
    price = models.IntegerField(verbose_name='цена', **NULLABLE)

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class CourseSubscribe(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return f"{self.course} - {self.user}"

    class Meta:
        verbose_name = 'подписка на курс'
        verbose_name_plural = 'подписки на курс'
