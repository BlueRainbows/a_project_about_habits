from rest_framework.generics import (ListAPIView, CreateAPIView,
                                     UpdateAPIView, DestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from habits.models import Habits
from habits.pagination import PaginationHabits
from habits.permissions import PermissionUser
from habits.serializers.habits import HabitsSerializer


class HabitsListAllView(ListAPIView):
    """ Список общедоступных привычек """
    queryset = Habits.objects.all().filter(publish=True)
    serializer_class = HabitsSerializer


class HabitsListPersonalView(ListAPIView):
    """ Список личных привычек """

    serializer_class = HabitsSerializer
    pagination_class = PaginationHabits

    def get_queryset(self):
        queryset = Habits.objects.filter(user=self.request.user)
        return queryset


class HabitsCreateView(CreateAPIView):
    """ Создание привычки """
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer

    def perform_create(self, serializer):
        """ Присвоение к привычке создателя """
        habits = serializer.save(user=self.request.user)
        habits.save()


class HabitsUpdateView(UpdateAPIView):
    """ Изменение привычки """
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated & PermissionUser]

    def perform_update(self, serializer):
        """ Присвоение к привычке создателя """
        habits = serializer.save(user=self.request.user)
        habits.save()


class HabitsDestroyView(DestroyAPIView):
    """ Удаление привычки """
    queryset = Habits.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = [IsAuthenticated & PermissionUser]
