from django.db import models

from config import settings
from main_app.models import NULLABLE, Course, Lesson


class Payment(models.Model):
    PAYMENT_METHOD = [
        ('CASH', 'наличные'),
        ('TRANSFER_TO_ACCOUNT', 'перевод на счет')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь',
                             **NULLABLE)
    date_of_payment = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, verbose_name='способ оплаты')

    class Meta:
        verbose_name = 'способ оплаты'
        verbose_name_plural = 'способы оплаты'

    def __str__(self):
        return f'{self.user} способ оплаты: {self.paid_course if self.paid_course else self.paid_lesson}'
