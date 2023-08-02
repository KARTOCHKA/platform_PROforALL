from rest_framework import status

from main_app.tests.main_app_tests import UserCreate


class LessonCreateTestCase(UserCreate):
    """Тестирование создания урока"""
    def create_lesson(self):
        response = self.client.post(
            '/lesson/create/',
            {'title': 'Вводный урок', 'course': self.course, 'video': 'https://www.youtube.com/@skypro-917'}
        )
        return response

    def test_lesson_create_unauth_user(self):
        """Тестирование создания урока для неавторизованного пользователя"""
        response = self.create_lesson()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_create_auth_user(self):
        """Тестирование создания урока для авторизованного пользователя"""
        self.lesson_for_auth_user()
        response = self.create_lesson()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_is_staff_user(self):
        """Тестирование создания урока для модератора"""
        self.course_for_is_staff_user()
        response = self.create_lesson()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_error_creating_lesson(self):
        """Тестирование валидации названия видео"""
        self.course_for_is_staff_user()
        response = self.client.post(
            '/lesson/create/',
            {'title': 'Вводный урок', 'course': self.course, 'video': 'https://www.sky.pro'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LessonListTestCase(UserCreate):
    """Тестирование просмотра уроков"""
    def get_lesson(self):
        response = self.client.get('/lesson/', )
        return response

    def test_get_lesson_unauth_user(self):
        """Тестирование просмотра уроков для неавторизованного пользователя"""
        response = self.get_lesson()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_get_lesson_auth_user(self):
        """Тестирование просмотра уроков для авторизованного пользователя"""
        self.lesson_for_auth_user()
        response = self.get_lesson()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{'title': 'test_lesson',
                          'preview': None,
                          'description': 'description_lesson',
                          'video': 'https://www.youtube.com/@skypro-917',
                          'course': 'test'}]}
        )

    def test_get_lesson_is_staff_user(self):
        """Тестирование просмотра уроков для модератора"""
        self.lesson_for_is_staff_user()
        response = self.get_lesson()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{'title': 'test_lesson',
                          'preview': None,
                          'description': 'description_lesson',
                          'video': 'https://www.youtube.com/@skypro-917',
                          'course': 'test'}]}
        )


class LessonRetrieveTestCase(UserCreate):
    """Тестирование просмотра одного урока"""
    def retrieve_lesson(self, lesson_id):
        return self.client.get(f'/lesson/{lesson_id}/', )

    def test_retrieve_lesson_unauth_user(self):
        """Тестирование просмотра одного урока для неавторизованного пользователя"""
        response = self.retrieve_lesson(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_retrieve_lesson_auth_user(self):
        """Тестирование просмотра одного урока для авторизованного пользователя"""
        lesson = self.lesson_for_auth_user()
        response = self.retrieve_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'title': 'test_lesson',
             'preview': None,
             'description': 'description_lesson',
             'video': 'https://www.youtube.com/@skypro-917',
             'course': 'test'}
        )

    def test_retrieve_lesson_is_staff_user(self):
        """Тестирование просмотра одного урока для модератора"""
        lesson = self.lesson_for_is_staff_user()
        response = self.retrieve_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'title': 'test_lesson',
             'preview': None,
             'description': 'description_lesson',
             'video': 'https://www.youtube.com/@skypro-917',
             'course': 'test'}
        )


class LessonUpdateTestCase(UserCreate):
    """Тестирование обновления урока"""
    def update_lesson(self, course_id):
        return self.client.patch(f'/lesson/update/{course_id}/',
                                 {'title': 'NEW_LESSON',
                                  'video': 'https://www.youtube.com/new_video'}
                                 )

    def test_update_lesson_unauth_user(self):
        """Тестирование обновления урока для неавторизованного пользователя"""
        response = self.update_lesson(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_update_lesson_auth_user(self):
        """Тестирование обновления урока для авторизованного пользователя"""
        lesson = self.lesson_for_auth_user()
        response = self.update_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'title': 'NEW_LESSON',
             'preview': None,
             'description': 'description_lesson',
             'video': 'https://www.youtube.com/new_video',
             'course': 'test'}
        )

    def test_update_lesson_is_staff_user(self):
        """Тестирование обновления урока для модератора"""
        lesson = self.lesson_for_is_staff_user()
        response = self.update_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'title': 'NEW_LESSON',
             'preview': None,
             'description': 'description_lesson',
             'video': 'https://www.youtube.com/new_video',
             'course': 'test'}
        )


class LessonDeleteTestCase(UserCreate):
    """Тестирование удаления урока"""
    def delete_lesson(self, lesson_id):
        return self.client.delete(f'/lesson/delete/{lesson_id}/',)

    def test_delete_lesson_unauth_user(self):
        """Тестирование удаления урока для неавторизованного пользователя"""
        response = self.delete_lesson(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'}
        )

    def test_delete_lesson_auth_user(self):
        """Тестирование удаления урока для авторизованного пользователя"""
        lesson = self.lesson_for_auth_user()
        response = self.delete_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_is_staff_user(self):
        """Тестирование удаления урока для модератора"""
        lesson = self.lesson_for_auth_user()
        response = self.delete_lesson(lesson.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
