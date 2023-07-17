from django.urls import path
from rest_framework.routers import DefaultRouter

from main_app.views import *

router = DefaultRouter()
router.register(r'main_app', CourseViewSet, basename='main_app')


urlpatterns = [
    path('lesson/', LessonListView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>', LessonDeleteAPIView.as_view(), name='lesson_delete')
] + router.urls
