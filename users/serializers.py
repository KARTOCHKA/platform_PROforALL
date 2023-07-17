from rest_framework import serializers
from users.models import User
from payment.serializers import PaymentSerializer


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'name', 'phone', 'city', 'avatar']

    def save(self, *args, **kwargs):
        """Метод для сохранения нового пользователя"""
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],
            name=self.validated_data['name'],
            phone=self.validated_data['phone'],
            city=self.validated_data['city'],
            avatar=self.validated_data['avatar'],
        )
        # Проверяем на валидность пароли
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = '__all__'


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'city', 'avatar')
