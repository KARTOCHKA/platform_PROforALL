from main_app.models import CourseSubscription
from payment.models import Payment


def check_payment_status_and_activate_subscription(course_id, user):
    """Проверяет статус платежа и если она активна меняет флаг активности подписки"""
    payment = Payment.objects.filter(paid_course=course_id, user=user)
    if payment.exists():
        print(payment.first().status)
        if payment.first().status == 'succeeded':
            subscription = CourseSubscription.objects.filter(user=user, course=course_id).first()
            subscription.activate()


def update_subscriptions():
    pass
