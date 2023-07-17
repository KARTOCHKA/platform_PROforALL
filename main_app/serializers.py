from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from main_app.models import *


class LessonSerializer(serializers.ModelSerializer):
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'preview', 'description', 'video', 'course')


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = serializers.SerializerMethodField()

    @staticmethod
    def get_lessons_count(obj):
        lessons = Lesson.objects.filter(course=obj).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = '__all__'
