from datetime import datetime, timedelta
from celery import shared_task

from habits.models import Habits
from habits.services import create_message


@shared_task()
def every_day_habits():
    """
    Фильтрует модель habits по переодичности и исключает пользователей,
    у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Определяет время отправки уведовления пользователю,
    с минутным промежутком.
    """
    habits = (Habits.objects.filter(periodicity='Каждый день').
              exclude(user__telegram_id=None))

    for every_day in habits:
        time_max = datetime.now() + timedelta(seconds=30)
        time_min = datetime.now() - timedelta(seconds=30)
        if time_min.time() <= every_day.time <= time_max.time():
            create_message(every_day)


@shared_task()
def every_few_days_habits():
    """
    Фильтрует модель habits по переодичности, времени
    и исключает пользователей, у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Определяет дату отправки уведовления пользователю,
    с минутным промежутком,
    если уведомление было отправлено ранее.
    Иначе отправляет уведовление пользователю
    и определяет время для следующей отправки уведовления.
    """
    time_max = datetime.now() + timedelta(seconds=30)
    time_min = datetime.now() - timedelta(seconds=30)
    habits = (
        Habits.objects.filter(
            periodicity='Раз в несколько дней'
        ).
        exclude(
            user__telegram_id=None
        ).
        filter(
            time__lte=time_max.time(),
            time__gte=time_min.time()
        )
    )
    for habit in habits:
        if habit.last_notification:
            if (habit.last_notification.date()
                    == datetime.now().date()):

                create_message(habit)
                habit.last_notification = (
                        habit.last_notification
                        + timedelta(days=2))
                habit.save()
        else:
            create_message(habit)
            habit.last_notification = (
                    datetime.now() + timedelta(days=2))
            habit.save()


@shared_task()
def every_week_habits():
    """
    Фильтрует модель habits по переодичности, времени
    и исключает пользователей, у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Определяет дату отправки уведовления пользователю,
    с минутным промежутком,
    если уведомление было отправлено ранее.
    Иначе отправляет уведовление пользователю
    и определяет время для следующей отправки уведовления.
    """
    time_max = datetime.now() + timedelta(seconds=30)
    time_min = datetime.now() - timedelta(seconds=30)
    habits = (
        Habits.objects.filter(
            periodicity='Раз в неделю'
        ).
        exclude(
            user__telegram_id=None
        ).
        filter(
            time__lte=time_max.time(),
            time__gte=time_min.time()
        )
    )
    for habit in habits:
        if habit.last_notification:
            if (habit.last_notification.date()
                    == datetime.now().date()):

                create_message(habit)
                habit.last_notification = (
                        habit.last_notification
                        + timedelta(days=7))
                habit.save()
        else:
            create_message(habit)
            habit.last_notification = (
                    datetime.now() + timedelta(days=7))
            habit.save()
