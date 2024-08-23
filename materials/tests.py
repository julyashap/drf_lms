from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_owner = User.objects.create(email="test_owner@test.ru", password="test_password")

        self.user_moderator = User.objects.create(email="test_moderator@test.ru", password="test_password")
        group = Group.objects.create(name="moderators")
        self.user_moderator.groups.add(group)

        self.standart_user = User.objects.create(email="test_standart@test.ru", password="test_password")

        self.course = Course.objects.create(name="test-course", description="test-course")

        self.lesson = Lesson.objects.create(name="test-lesson", description="test-lesson", course=self.course,
                                            owner=self.user_owner)

    def test_authenticated_user(self):
        response = self.client.get(reverse('materials:retrieve_lesson', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson(self):
        data = {
            "name": "test-lesson",
            "description": "test-lesson https://www.youtube.com/",
            "video": "https://www.youtube.com/",
            "course": self.course.pk
        }

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.post(reverse('materials:create_lesson'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "id": self.lesson.pk + 1,
            "name": "test-lesson",
            "preview": None,
            "description": "test-lesson https://www.youtube.com/",
            "video": "https://www.youtube.com/",
            "course": self.course.pk,
            "owner": self.user_owner.pk
        })

        # тестирование метода модератором
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.post(reverse('materials:create_lesson'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_with_error(self):
        data_description_error = {
            "name": "test-lesson-desc",
            "description": "test-lesson-desc https://my.sky.pro/",
            "course": self.course.pk
        }

        data_video_error = {
            "name": "test-lesson",
            "description": "test-lesson",
            "video": "https://my.sky.pro/",
            "course": self.course.pk
        }

        self.client.force_authenticate(user=self.user_owner)

        response = self.client.post(reverse('materials:create_lesson'), data=data_description_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('materials:create_lesson'), data=data_video_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_lesson(self):
        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('materials:retrieve_lesson', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": self.lesson.pk,
            "name": "test-lesson",
            "preview": None,
            "description": "test-lesson",
            "video": None,
            "course": self.course.pk,
            "owner": self.user_owner.pk
        })

        # тестирование метода модератором
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(reverse('materials:retrieve_lesson', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": self.lesson.pk,
            "name": "test-lesson",
            "preview": None,
            "description": "test-lesson",
            "video": None,
            "course": self.course.pk,
            "owner": self.user_owner.pk
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.get(reverse('materials:retrieve_lesson', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_lesson(self):
        Lesson.objects.create(name="test-lesson", description="test-lesson",
                              course=self.course)

        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.get(reverse('materials:list_lesson'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "test-lesson",
                    "preview": None,
                    "description": "test-lesson",
                    "video": None,
                    "course": self.course.pk,
                    "owner": self.user_owner.pk
                }
            ]
        })

        # тестирование метода модератором
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.get(reverse('materials:list_lesson'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "test-lesson",
                    "preview": None,
                    "description": "test-lesson",
                    "video": None,
                    "course": self.course.pk,
                    "owner": self.user_owner.pk
                },
                {
                    "id": self.lesson.pk + 1,
                    "name": "test-lesson",
                    "preview": None,
                    "description": "test-lesson",
                    "video": None,
                    "course": self.course.pk,
                    "owner": None
                },
            ]
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.get(reverse('materials:list_lesson'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        })

    def test_update_lesson(self):
        # тестирование метода владельцем
        data = {
            "name": "test-lesson-new",
            "description": "test-lesson-new https://www.youtube.com/",
            "video": "https://www.youtube.com/",
            "course": self.course.pk
        }

        self.client.force_authenticate(user=self.user_owner)
        response = self.client.put(reverse('materials:update_lesson', kwargs={'pk': self.lesson.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": self.lesson.pk,
            "name": "test-lesson-new",
            "preview": None,
            "description": "test-lesson-new https://www.youtube.com/",
            "video": "https://www.youtube.com/",
            "course": self.course.pk,
            "owner": self.user_owner.pk
        })

        # тестирование метода модератором
        data = {
            "name": "test-lesson-new-new",
            "description": "test-lesson-new-new https://www.youtube.com/",
            "video": "https://www.youtube.com/1",
            "course": self.course.pk
        }

        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.put(reverse('materials:update_lesson', kwargs={'pk': self.lesson.pk}), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            "id": self.lesson.pk,
            "name": "test-lesson-new-new",
            "preview": None,
            "description": "test-lesson-new-new https://www.youtube.com/",
            "video": "https://www.youtube.com/1",
            "course": self.course.pk,
            "owner": self.user_owner.pk
        })

        # тестирование метода пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.put(reverse('materials:update_lesson', kwargs={'pk': self.lesson.pk}), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_lesson(self):
        # тестирование метода владельцем
        self.client.force_authenticate(user=self.user_owner)
        response = self.client.delete(reverse('materials:destroy_lesson', kwargs={'pk': self.lesson.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # тестирование метода модератором
        self.client.force_authenticate(user=self.user_moderator)
        response = self.client.delete(reverse('materials:destroy_lesson', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # тестирование метода обычным пользователем
        self.client.force_authenticate(user=self.standart_user)
        response = self.client.delete(reverse('materials:destroy_lesson', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CourseSubscribeTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru", password="test_password")
        self.course = Course.objects.create(name="test-course", description="test-course")

    def test_post(self):
        data = {
            "course": self.course.pk
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('materials:manage_course_subscribe'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            "id": 1,
            "user": self.user.pk,
            "course": self.course.pk
        })

        response = self.client.post(reverse('materials:manage_course_subscribe'), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка удалена!"})
