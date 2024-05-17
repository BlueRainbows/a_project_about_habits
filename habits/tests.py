from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User

PLEASANT_HABITS = {
    'place': 'Кухня',
    'time': '15:00:00',
    'action': 'Съесть пиццу',
    'publish': 'True',
    'sign_pleasant_habit': 'True',
}

USEFUL_HABITS = {
    'place': 'Ванная комната',
    'time': '11:00:00',
    'action': 'Умыться',
    'award': 'Ощутить бодрость',
}

USER_1 = {'email': 'Karina@Sapojkina.ru'}

USER_2 = {'email': 'Marina@Garmojkina.ru'}


class HabitsTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user_1 = User.objects.create(**USER_1)
        self.pleasant_habit = (
            Habits.objects.create(user=self.user_1, **PLEASANT_HABITS))
        self.useful_habit = (
            Habits.objects.create(user=self.user_1, **USEFUL_HABITS))
        self.client.force_authenticate(user=self.user_1)

    def test_getting_list_all_habits(self):
        """
        Тестирование получения списка опубликованных привычек
        """
        url = reverse('habits:habits_list_all')
        response = self.client.get(url)
        content = response.json()

        # Тест на удачное обращение к привычкам
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

        # Тест на равенство колличества опубликованного контента
        self.assertEqual(
            len(content), 1)

    def test_getting_list_personal_habits(self):
        """
        Тестирование получения списка личных привычек
        """
        url = reverse('habits:habits_list_personal')
        response = self.client.get(url)
        content = response.json()

        # Тест на удачное обращение к привычкам
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

        # Тест на авторство привычки у пользователя
        self.assertEqual(
            content.get('results')[0].get('user'), self.user_1.id)

        # Тест на равенство колличества привычек у текущего пользователя
        self.assertEqual(
            content.get('count'), 2)

    def test_creating_habits(self):
        """
        Тестирование создания привычки
        """
        url = reverse('habits:habits_create')
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
            'periodicity': 'Раз в неделю',
        }
        response = self.client.post(path=url, data=data, format='json')

        # Тест на удачное создание урока
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED)

        # Тест на колличество уроков
        self.assertEqual(
            Habits.objects.count(), 3)

        # Тест на прикрепление авторства на урок
        self.assertEqual(
            Habits.objects.get(action='Съесть сырок').user, self.user_1)

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:03:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
        }
        response = self.client.post(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации времени на выполнение привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['Время на выполнение не может превышать 2-ух минут'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'award': 'Получить удовольствие',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
        }
        response = self.client.post(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации вознаграждения для приятной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['У приятной привычки не может быть вознаграждения'
             ' или связанной привычки'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
            'pleasant_habit': self.pleasant_habit.id,
        }
        response = self.client.post(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации добавления связной привычки
        # для приятной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['У приятной привычки не может быть вознаграждения'
             ' или связанной привычки'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'pleasant_habit': self.useful_habit.id,
        }
        response = self.client.post(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации связной привычки для полезной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['Вы можете добавить только приятную привычку'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'publish': 'True',
        }
        response = self.client.post(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации связной привычки для полезной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ["Периодичность привычки не может быть пустой. "
                "Выберите из вариантов: "
                "Каждый день, Раз в несколько дней, Раз в неделю"])

    def test_update_habits(self):
        """
        Тестирование изменения привычек
        """
        url = reverse('habits:habits_update',
                      kwargs={'pk': self.useful_habit.pk})
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'pleasant_habit': self.pleasant_habit.id,
        }
        response = self.client.patch(path=url, data=data, format='json')
        content = response.json()

        # Тест на удачное изменение привычки
        self.assertEqual(
            response.status_code, status.HTTP_200_OK)

        # Тест на удачное изменение связной привычки у полезной
        self.assertEqual(
            content.get('pleasant_habit'), self.pleasant_habit.id)

        ##########################################################
        url = reverse('habits:habits_update',
                      kwargs={'pk': self.pleasant_habit.pk})
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:03:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
        }
        response = self.client.patch(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации времени на выполнение привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['Время на выполнение не может превышать 2-ух минут'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'award': 'Получить удовольствие',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
        }
        response = self.client.patch(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации вознаграждения для приятной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['У приятной привычки не может быть вознаграждения'
             ' или связанной привычки'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'periodicity': 'Раз в неделю',
            'publish': 'True',
            'sign_pleasant_habit': 'True',
            'pleasant_habit': self.pleasant_habit.id,
        }
        response = self.client.patch(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации добавления связной привычки
        # для приятной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ['У приятной привычки не может быть вознаграждения'
             ' или связанной привычки'])

        ##########################################################
        data = {
            'user': self.user_1.id,
            'place': 'Кухня',
            'time': '16:00:00',
            'action': 'Съесть сырок',
            'time_to_complete': '00:02:00',
            'publish': 'True',
        }
        response = self.client.patch(path=url, data=data, format='json')
        resp = response.json()

        # Тест на ошибку валидации связной привычки для полезной привычки
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            resp.get('non_field_errors'),
            ["Периодичность привычки не может быть пустой. "
             "Выберите из вариантов: "
             "Каждый день, Раз в несколько дней, Раз в неделю"])

    def test_delete_habits(self):
        """
        Тестирование удаление привычек
        """
        url = reverse('habits:habits_destroy',
                      kwargs={'pk': self.pleasant_habit.pk})
        response = self.client.delete(path=url)

        # Тест на удачное удаление урока
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT)
