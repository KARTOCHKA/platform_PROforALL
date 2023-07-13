from rest_framework import serializers

from main_app.models import *


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        lessons = Lesson.objects.filter(course=obj).all()
        if lessons:
            return lessons.count()
        return 0

    class Meta:
        model = Course
        fields = ('id', 'title', 'preview', 'description', 'lessons', 'lessons_count')
