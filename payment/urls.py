from django.urls import path

from payment.views import *

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment_list'),
    path('<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_detail'),
    path('payment-intent/create/', PaymentIntentCreateView.as_view(), name='payment_intent_create'),
    path('payment-method/confirm/', PaymentIntentConfirmView.as_view(), name='payment_method_confirm')
]