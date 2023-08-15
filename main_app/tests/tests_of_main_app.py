from rest_framework import status

from main_app.tests.services import UserCreate


class CourseCreateTestCase(UserCreate):
    """Тестирование создания курса"""

    def create_course(self):
        response = self.client.post('/course/', {'title': 'Python'})
        return response

    def test_course_create_unauth_user(self):
        """Тестирование создания курса для неавторизованного пользователя"""
        response = self.create_course()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_create_auth_user(self):
        """Тестирование создания курса для авторизованного пользователя"""
        self.course_for_auth_user()
        response = self.create_course()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_create_is_staff_user(self):
        """Тестирование создания курса для модератора"""
        self.course_for_is_staff_user()
        response = self.create_course()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CourseListTestCase(UserCreate):
    """Тестирование просмотра курсов"""

    def get_course(self):
        response = self.client.get('/course/', )
        return response

    def test_get_course_unauth_user(self):
        """Тестирование просмотра курсов для неавторизованного пользователя"""
        response = self.get_course()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_get_course_auth_user(self):
        """Тестирование просмотра курсов для авторизованного пользователя"""
        self.course_for_auth_user()
        response = self.get_course()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{'title': 'test',
                          'description': 'description',
                          'lessons': [{'title': 'test_lesson',
                                       'preview': None,
                                       'description': 'description_lesson',
                                       'video': 'https://www.youtube.com/@skypro-917',
                                       'course': 'test'}],
                          'lessons_count': 1,
                          'subscription': [
                              {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}]}
        )

    def test_get_course_is_staff_user(self):
        """Тестирование просмотра курсов для модератора"""
        self.course_for_is_staff_user()
        response = self.get_course()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'count': 1,
             'next': None,
             'previous': None,
             'results': [{'title': 'test',
                          'description': 'description',
                          'lessons': [{'title': 'test_lesson',
                                       'preview': None,
                                       'description': 'description_lesson',
                                       'video': 'https://www.youtube.com/@skypro-917',
                                       'course': 'test'}],
                          'lessons_count': 1,
                          'subscription': [
                              {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}]}
        )


class CourseRetrieveTestCase(UserCreate):
    """Тестирование просмотра одного курса"""

    def retrieve_course(self, course_id):
        return self.client.get(f'/course/{course_id}/', )

    def test_retrieve_course_unauth_user(self):
        """Тестирование просмотра одного курса для неавторизованного пользователя"""
        response = self.retrieve_course(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_retrieve_course_auth_user(self):
        """Тестирование просмотра одного курса для авторизованного пользователя"""
        course = self.course_for_auth_user()
        response = self.retrieve_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'title': 'test',
             'description': 'description',
             'lessons': [
                 {'title': 'test_lesson',
                  'preview': None,
                  'description': 'description_lesson',
                  'video': 'https://www.youtube.com/@skypro-917',
                  'course': 'test'}],
             'lessons_count': 1,
             'subscription': [
                 {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}
        )

    #
    def test_retrieve_course_is_staff_user(self):
        """Тестирование просмотра одного курса для модератора"""
        course = self.course_for_is_staff_user()
        response = self.retrieve_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'title': 'test',
             'description': 'description',
             'lessons': [{'title': 'test_lesson',
                          'preview': None,
                          'description': 'description_lesson',
                          'video': 'https://www.youtube.com/@skypro-917',
                          'course': 'test'}],
             'lessons_count': 1,
             'subscription': [
                 {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}
        )


class CourseUpdateTestCase(UserCreate):
    """Тестирование обновления курса"""

    def update_course(self, course_id):
        return self.client.patch(f'/course/{course_id}/', {'title': 'new_test'})

    def test_update_course_unauth_user(self):
        """Тестирование обновления курса для неавторизованного пользователя"""
        response = self.update_course(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_update_course_auth_user(self):
        """Тестирование обновления курса для авторизованного пользователя"""
        course = self.course_for_auth_user()
        response = self.update_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {'title': 'new_test',
             'description': 'description',
             'lessons': [{'title': 'test_lesson',
                          'preview': None,
                          'description': 'description_lesson',
                          'video': 'https://www.youtube.com/@skypro-917',
                          'course': 'new_test'}],
             'lessons_count': 1,
             'subscription': [
                 {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}
        )

    def test_update_course_is_staff_user(self):
        """Тестирование обновления курса для модератора"""
        course = self.course_for_is_staff_user()
        response = self.update_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {'title': 'new_test',
             'description': 'description',
             'lessons': [{'title': 'test_lesson',
                          'preview': None,
                          'description': 'description_lesson',
                          'video': 'https://www.youtube.com/@skypro-917',
                          'course': 'new_test'}],
             'lessons_count': 1,
             'subscription': [
                 {'version': '1', 'user': None, 'course': self.course.pk, 'is_active': False}]}
        )


#
class CourseDeleteTestCase(UserCreate):
    """Тестирование удаления курса"""

    def delete_course(self, course_id):
        return self.client.delete(f'/course/{course_id}/', )

    def test_delete_course_unauth_user(self):
        """Тестирование удаления курса для неавторизованного пользователя"""
        response = self.delete_course(1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

    def test_delete_course_auth_user(self):
        """Тестирование удаления курса для авторизованного пользователя"""
        course = self.course_for_auth_user()
        response = self.delete_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_course_is_staff_user(self):
        """Тестирование удаления курса для модератора"""
        course = self.course_for_is_staff_user()
        response = self.delete_course(course.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
