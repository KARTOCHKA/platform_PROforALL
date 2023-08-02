from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from main_app.models import *
from main_app.validations import VideoValidator


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
        fields = ('user', 'course', 'is_active')


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
