from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from main_app.permissions import IsModerator, IsOwner
from payment.serializers import *
from payment.services import PaymentService


class PaymentIntentCreateView(generics.CreateAPIView):
    """Создание платежного намерения"""
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentIntentCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            course_id = serializer.validated_data['course_id']
            user = self.request.user
            try:
                payment_intent = PaymentService.create_payment_intent(course_id=course_id, user=user)
                payment = Payment.objects.filter(id_payment_intent=payment_intent['id']).first()
                payment_serializer = PaymentSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentIntentConfirmView(generics.CreateAPIView):
    """Подтверждение платежа"""
    serializer_class = PaymentIntentConfirmSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            id_payment_intent = serializer.validated_data['id_payment_intent']
            payment_token = serializer.validated_data['payment_token']
            try:
                # создание метода платежа
                payment_method = PaymentService.create_payment_method(payment_token)
                # привязка метода платежа к платежному намерению
                PaymentService.connect_payment_intent_and_method(payment_method_id=payment_method["id"],
                                                                 id_payment_intent=id_payment_intent)
                # подтверждение платежа
                PaymentService.confirm_payment_intent(id_payment_intent)
                payment = Payment.objects.filter(id_payment_intent=id_payment_intent).first()
                # изменение статуса платежа на "Оплачено"
                payment.change_is_paid()
                payment_serializer = PaymentListSerializer(payment)
                return Response(payment_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentListAPIView(generics.ListAPIView):
    """Представления для просмотра списка платежей"""
    queryset = Payment.objects.all()
    serializer_class = PaymentListSerializer
    permission_classes = [IsModerator | IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', ]
    ordering_fields = ['date_of_payment']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentListSerializer
    permission_classes = [IsModerator | IsOwner]
    queryset = Payment.objects.all()