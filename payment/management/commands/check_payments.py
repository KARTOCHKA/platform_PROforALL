from django.core.management import BaseCommand

from payment.tasks import check_payment_status


class Command(BaseCommand):
    """Запускает проверку статуса платежей при вызове в консоли команды:
       python3 manage.py check_payments"""
    def handle(self, *args, **options):
        check_payment_status()