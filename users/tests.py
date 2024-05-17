from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User

USER_1 = {'email': 'Karina@Sapojkina.ru'}


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = User.objects.create(**USER_1)
        self.client.force_authenticate(user=self.user_1)

    def test_profile_update(self):
        url = reverse('users:profile',
                      kwargs={'pk': self.user_1.pk})
        data = {
            'email': 'Karina@Sapojkina.ru',
            'telegram_id': '123',
            'password': '1548'
        }
        response = self.client.patch(path=url, data=data, format='json')
        content = response.json()

        # Тест на удачное изменение
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

        # Тест на удачное изменение telegram_id
        self.assertEqual(
            content.get('telegram_id'), '123')
