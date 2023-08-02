from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from main_app.models import Course, Lesson, CourseSubscription
from main_app.paginations import MaterialPagination
from main_app.permissions import IsModerator, IsOwner
from main_app.serializers import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """Представление курса, которое включает в себя механизм CRUD"""
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MaterialPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Course.objects.all()
        else:
            return Course.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonListView(generics.ListAPIView):
    """Представление списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = MaterialPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(user=user)


class LessonDetailAPIView(generics.RetrieveAPIView):
    """Представление для одного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Представление для обновления урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDeleteAPIView(generics.DestroyAPIView):
    """Представление для удаления урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class CourseSubscriptionListAPIView(generics.ListAPIView):
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CourseSubscription.objects.all()
        else:
            return CourseSubscription.objects.filter(user=user)


class CourseSubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseSubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = CourseSubscription.objects.all()
    serializer_class = CourseSubscriptionSerializer
    permission_classes = [IsAuthenticated, IsOwner]
