from django.db import models

from config import settings
from main_app.models import NULLABLE, Course


class Payment(models.Model):
    """Модель для способа оплаты урока или курса"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='пользователь',
                             **NULLABLE)
    date_of_payment = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс', **NULLABLE)
    payment_amount = models.IntegerField(verbose_name='сумма оплаты', **NULLABLE)
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    id_payment_intent = models.CharField(max_length=300, **NULLABLE, verbose_name='id намерения платежа')
    id_payment_method = models.CharField(max_length=300, **NULLABLE, verbose_name='id метода платежа')
    status = models.CharField(max_length=50, **NULLABLE, verbose_name='статус платежа')

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплаты'

    def __str__(self):
        return f'{self.user} (курс {self.paid_course})'

    def change_is_paid(self):
        self.is_paid = True
        self.save()
