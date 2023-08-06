from rest_framework import status

from main_app.tests.main_app_tests import UserCreate


class CourseSubscriptionCreateTestCase(UserCreate):
    """Тестирование создания подписки на курс"""

    def course_subscription_create(self):
        response = self.client.post('/subscription/create/', {'version': '2', 'course': self.course.id})
        return response

    def test_course_subscription_create_unauth_user(self):
        """Тестирование создания подписки на курс для неавторизованного пользователя"""
        response = self.course_subscription_create()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_subscription_create_auth_user(self):
        """Тестирование создания подписки на курс для авторизованного пользователя"""
        self.course_subscription_for_auth_user()
        response = self.course_subscription_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_subscription_is_staff_user(self):
        """Тестирование создания курса для модератора"""
        self.course_subscription_for_is_staff_user()
        response = self.course_subscription_create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourseSubscriptionListTestCase(UserCreate):
    """Тестирование просмотра подписки на курс"""

    def get_course_subscription(self):
        response = self.client.get('/subscription/', )
        return response

    def test_get_course_subscription_unauth_user(self):
        """Тестирование просмотра подписки на курс для неавторизованного пользователя"""
        response = self.get_course_subscription()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_get_course_subscription_auth_user(self):
        """Тестирование просмотра подписки на курс для авторизованного пользователя"""
        self.course_subscription_for_auth_user()
        response = self.get_course_subscription()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_course_subscription_is_staff_user(self):
        """Тестирование просмотра подписки на курс для модератора"""
        self.course_subscription_for_is_staff_user()
        response = self.get_course_subscription()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         [{'version': '1', 'user': self.user.pk, 'course': self.course.pk, 'is_active': False}])


class CourseSubscriptionDeleteTestCase(UserCreate):
    """Тестирование удаления подписки на курс"""

    def delete_course_subscription(self, course_id):
        return self.client.delete(f'/subscription/delete/{course_id}/', )

    def test_delete_course_subscription_unauth_user(self):
        """Тестирование удаления подписки на курс для неавторизованного пользователя"""
        response = self.delete_course_subscription(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_delete_course_subscription_auth_user(self):
        """Тестирование удаления подписки на курс для авторизованного пользователя"""
        course = self.course_subscription_for_auth_user()
        response = self.delete_course_subscription(course.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_subscription_is_staff_user(self):
        """Тестирование удаления подписки на курс для модератора"""
        course = self.course_subscription_for_is_staff_user()
        response = self.delete_course_subscription(course.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
