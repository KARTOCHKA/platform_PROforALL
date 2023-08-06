from celery import shared_task
from payment.models import Payment
from payment.services import PaymentService


@shared_task
def check_payment_status() -> None:
    """Проверяет и обновляет статус неподтвержденных платежей"""
    payments = Payment.objects.filter(is_paid=False)
    if payments.exists():
        for payment in payments:
            PaymentService.confirm_payment_intent(id_payment_intent=payment.id_payment_intent)
