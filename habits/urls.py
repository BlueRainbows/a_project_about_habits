from django.urls import path

from habits.apps import HabitsConfig
import habits.views

app_name = HabitsConfig.name


urlpatterns = [
    # Список общедоступных привычек
    path('',
         habits.views.HabitsListAllView.as_view(),
         name='habits_list_all'),
    # Список личных привычек
    path('habits/list/',
         habits.views.HabitsListPersonalView.as_view(),
         name='habits_list_personal'),
    # Создание привычки
    path('habits/create/',
         habits.views.HabitsCreateView.as_view(),
         name='habits_create'),
    # Просмотр привычки
    path('habits/detail/<int:pk>/',
         habits.views.HabitsRetrieveAPIView.as_view(),
         name='habits_detail'),
    # Изменение привычки
    path('habits/update/<int:pk>/',
         habits.views.HabitsUpdateView.as_view(),
         name='habits_update'),
    # Удаление привычки
    path('habits/delete/<int:pk>/',
         habits.views.HabitsDestroyView.as_view(),
         name='habits_destroy'),
]
