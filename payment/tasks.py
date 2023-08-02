from celery import shared_task


@shared_task
def check_payment_status() -> None:
    """Проверяет и обновляет статус неподтвержденных платежей"""
    from payment.models import Payment
    from payment.services import PaymentService
    payments = Payment.objects.filter(is_paid=False)

    for payment in payments:
        PaymentService.confirm_payment_intent(id_payment_intent=payment.id_payment_intent)
