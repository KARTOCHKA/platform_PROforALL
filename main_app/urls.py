from django.urls import path
from rest_framework.routers import DefaultRouter

from main_app.views import *

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/detail/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int_pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>', LessonDeleteAPIView.as_view(), name='lesson_delete')
] + router.urls
