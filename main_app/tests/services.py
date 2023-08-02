from rest_framework.test import APITestCase

from main_app.models import Course, Lesson, CourseSubscription
from users.models import User


class UserCreate(APITestCase):
    def setUp(self):
        """Создание экземпляров курса, урока и подписки на курс"""
        self.course = Course.objects.create(title='test', description='description', )
        self.lesson = Lesson.objects.create(title='test_lesson',
                                            description='description_lesson',
                                            course=self.course,
                                            video='https://www.youtube.com/@skypro-917')
        self.subscription = CourseSubscription.objects.create(course=self.course)

    def create_user(self, is_staff):
        """Создание и авторизация пользователя"""
        self.email = 'example@test.ru'
        self.user = User(email=self.email, is_staff=is_staff)
        self.user.set_password('123Qaz')
        self.user.save()
        response = self.client.post(
            '/users/api/token/',
            {
                'email': self.email,
                'password': '123Qaz'
            }
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def create_auth_user(self):
        """Создание авторизованного пользователя"""
        self.create_user(is_staff=False)

    def create_is_staff_user(self):
        """Создание модератора"""
        self.create_user(is_staff=True)

    def course_for_auth_user(self):
        """Привязка авторизованного пользователя к курсу"""
        self.create_auth_user()
        self.course.user = self.user
        self.course.save()
        return self.course

    def course_for_is_staff_user(self):
        """Привязка модератора к курсу"""
        self.create_is_staff_user()
        self.course.user = self.user
        self.course.save()
        return self.course

    def lesson_for_auth_user(self):
        """Привязка авторизованного пользователя к уроку"""
        self.create_auth_user()
        self.lesson.user = self.user
        self.lesson.save()
        return self.lesson

    def lesson_for_is_staff_user(self):
        """Привязка модератора к уроку"""
        self.create_is_staff_user()
        self.lesson.user = self.user
        self.lesson.save()
        return self.lesson

    def course_subscription_for_auth_user(self):
        """Привязка авторизованного пользователя к уроку"""
        self.create_auth_user()
        self.subscription.user = self.user
        self.subscription.save()
        return self.subscription

    def course_subscription_for_is_staff_user(self):
        """Привязка модератора к уроку"""
        self.create_is_staff_user()
        self.subscription.user = self.user
        self.subscription.save()
        return self.subscription
