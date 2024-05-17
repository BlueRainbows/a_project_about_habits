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
    Фильтрует модель habits по переодичности и исключает пользователей,
    у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Определяет дату и время отправки уведовления пользователю,
    с минутным промежутком,
    если уведомление было отправлено ранее.
    Иначе определяет время для отправки уведовления пользователю.
    """
    habits = (Habits.objects.filter(periodicity='Раз в несколько дней').
              exclude(user__telegram_id=None))

    for every_few_days in habits:
        if every_few_days.last_notification:
            time_max = datetime.now() + timedelta(seconds=30)
            time_min = datetime.now() - timedelta(seconds=30)
            if (every_few_days.last_notification.date()
                    == datetime.now().date()):
                if (time_min.time() <=
                        every_few_days.last_notification.time() <=
                        time_max.time()):
                    create_message(every_few_days)

                    every_few_days.last_notification = (
                                every_few_days.last_notification
                                + timedelta(days=2))

                    every_few_days.save()
            else:
                data = datetime.now()
                time_max = data + timedelta(seconds=30)
                time_min = data - timedelta(seconds=30)
                if (time_min.time() <=
                    every_few_days.time <=
                        time_max.time()):

                    create_message(every_few_days)

                    every_few_days.last_notification = data + timedelta(days=2)

                    every_few_days.save()


@shared_task()
def every_week_habits():
    """
    Фильтрует модель habits по переодичности и исключает пользователей,
    у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Определяет дату и время отправки уведовления пользователю,
    с минутным промежутком,
    если уведомление было отправлено ранее.
    Иначе определяет время для отправки уведовления пользователю.
    """
    habits = (Habits.objects.filter(periodicity='Раз в неделю').
              exclude(user__telegram_id=None))

    for every_week in habits:
        if every_week.last_notification:
            time_max = datetime.now() + timedelta(seconds=30)
            time_min = datetime.now() - timedelta(seconds=30)
            if (every_week.last_notification.date()
                    == datetime.now().date()):
                if (time_min.time() <=
                    every_week.last_notification.time() <=
                        time_max.time()):

                    create_message(every_week)

                    every_week.last_notification = (
                        every_week.last_notification
                        + timedelta(days=7))

                    every_week.save()
        else:
            data = datetime.now()
            time_max = data + timedelta(seconds=30)
            time_min = data - timedelta(seconds=30)
            if (time_min.time() <=
                every_week.time <=
                    time_max.time()):

                create_message(every_week)

                every_week.last_notification = data + timedelta(days=7)

                every_week.save()
