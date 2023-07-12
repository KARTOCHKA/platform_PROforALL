from django.db import models
from django.contrib.auth.models import AbstractUser
from main_app.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    name = models.CharField(max_length=50, verbose_name='имя', **NULLABLE)
    phone = models.CharField(max_length=50, verbose_name='телефон', **NULLABLE)
    city = models.CharField(max_length=50, verbose_name='город', **NULLABLE)
    avatar = models.ImageField(verbose_name='фото', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
