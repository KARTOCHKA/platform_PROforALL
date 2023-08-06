from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='название')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='пользователь')
    amount = models.IntegerField(default=0, verbose_name='цена')

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='название')
    preview = models.ImageField(verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    video = models.CharField(max_length=150, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                             verbose_name='пользователь')

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
        ordering = ('title',)

    def __str__(self):
        return self.title


class CourseSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь',
                             **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
    is_active = models.BooleanField(default=True, verbose_name='признак подписки')
    version = models.CharField(max_length=50, default=1, verbose_name='версия подписки')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'Подписка на курс {self.course} ({self.user})'

    def delete(self, **kwargs):
        """Отключение подписки"""
        self.is_active = False
        self.save()

    def update_version(self, version):
        self.version = version
        self.save()

    def activate(self):
        self.is_active = True
        self.save()
