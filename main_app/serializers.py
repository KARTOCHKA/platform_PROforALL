from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from main_app.models import *
from main_app.validations import VideoValidator
from main_app.services import check_payment_status_and_activate_subscription
from main_app.tasks import send_message_a_course_update


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    title = serializers.CharField(max_length=150)

    class Meta:
        model = Lesson
        fields = ('title', 'preview', 'description', 'video', 'course')
        validators = [VideoValidator(field='video')]


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для представления подписки на курс"""

    def get_user(self, value):
        return self.context['request'].user

    class Meta:
        model = CourseSubscription
        fields = ('version', 'user', 'course', 'is_active')

    def validate(self, attrs):
        """Проверяет, не дублируется ли подписка"""
        user = self.context['request'].user
        course = attrs['course']
        version = attrs['version']
        subscription = CourseSubscription.objects.filter(user=user, course=course, version=version).exists()

        if subscription:
            raise serializers.ValidationError(
                f"Подписка {version} на курс {course} у пользователя {user} уже существует")
        return attrs

    def create(self, validated_data):
        """Обновляет версию подписки, если она уже есть и создает, если ее не было"""
        user = self.context['request'].user
        course = validated_data['course']
        version = validated_data['version']
        subscip = CourseSubscription.objects.filter(user=user, course=course)
        if subscip.exists():
            subscip.first().update_version(version=version)
            # отправка письма при обновлении курса
            send_message_a_course_update.delay(course.title, version, user.email)
        else:
            CourseSubscription.objects.create(
                user=user,
                course=course,
                version=version
            )
        # меняется статус активности подписки, если она оплачена
        check_payment_status_and_activate_subscription(course_id=course.id, user=user)

        return validated_data


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscription = CourseSubscriptionSerializer(many=True, read_only=True, source='coursesubscription_set')
    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        lessons = Lesson.objects.filter(course=obj).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ('title', 'description', 'lessons', 'lessons_count', 'subscription')
