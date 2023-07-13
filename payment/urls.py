from django.urls import path

from payment.views import *

urlpatterns = [
    path('', PaymentListAPIView.as_view(), name='payment_list'),
    path('detail/<int:pk>/', PaymentDetailAPIView.as_view(), name='payment_detail'),
    path('create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('update/<int_pk>/', PaymentUpdateAPIView.as_view(), name='payment_update'),
    path('delete/<int:pk>', PaymentDeleteAPIView.as_view(), name='payment_delete')
]
