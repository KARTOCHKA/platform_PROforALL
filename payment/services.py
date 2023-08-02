import requests
import stripe

from config import settings
from main_app.models import Course
from payment.models import Payment


class PaymentService:
    """Класс, описывающий работу с сервисов Stripe"""
    # ключ для работы с сервисом
    api_key = settings.STRIPE_SECRET_KEY
    # заголовок для авторизации
    headers = {'Authorization': f'Bearer {api_key}'}
    # базовый url
    base_url = 'https://api.stripe.com/v1'

    @classmethod
    def create_payment_intent(cls, course_id, user):
        """Создание платежного намерения"""
        course = Course.objects.filter(id=course_id).first()
        print(course.amount)
        data = [
            ('amount', course.amount),
            ('currency', 'usd')
        ]
        response = requests.post(f'{cls.base_url}/payment_intents', headers=cls.headers, data=data)

        if response.status_code != 200:
            raise Exception(f'Ошибка создания намерения платежа {response.status_code}')

        payment_intent = response.json()

        Payment.objects.create(
            user=user,
            paid_course=course,
            payment_amount=course.amount,
            id_payment_intent=payment_intent['id'],
            status=payment_intent['status']
        )
        return payment_intent

    @classmethod
    def create_payment_method(cls, payment_token):
        """Cоздание метода платежа"""
        data = {
            'type': 'card',
            'card[token]': payment_token,
        }
        response = requests.post(f'{cls.base_url}/payment_methods', headers=cls.headers, data=data)
        payment_method = response.json()
        print(response.json())
        if response.status_code != 200:
            raise Exception(f'Ошибка создания метода платежа {response.status_code}')

        return payment_method


@classmethod
def connect_payment_intent_and_method(cls, payment_method_id, id_payment_intent):
    """Привязка метода платежа к намерению платежа"""
    data = {'payment_method': payment_method_id}
    response = requests.post(f'{cls.base_url}/payment_intents/{id_payment_intent}', headers=cls.headers, data=data)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(f'Ошибка в привязывании метода платежа к намерению {response.status_code}')

    payment = Payment.objects.filter(id_payment_intent=id_payment_intent).first()
    payment.id_payment_method = payment_method_id
    payment.status = response_data['status']
    payment.save()
    return response_data


@classmethod
def confirm_payment_intent(cls, id_payment_intent):
    """"Подтверждение платежа"""
    payment = Payment.objects.filter(id_payment_intent=id_payment_intent).first()
    data = {'payment_method': payment.id_payment_method}
    response = requests.post(f'{cls.base_url}/payment_intents/{id_payment_intent}/confirm',
                             headers=cls.headers,
                             data=data)
    response_data = response.json()
    if response.status_code != 200:
        raise Exception(f'Ошибка подтверждения платежа: {response.status_code}')

    payment.status = response_data['status']
    payment.save()
    return response_data
