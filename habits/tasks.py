from datetime import datetime, timedelta
from celery import shared_task

from habits.models import Habits
from habits.services import create_message


@shared_task()
def send_habits():
    """
    Фильтрует модель habits по времени отправки уведомления,
    исключает пользователей, у которых нет телеграм id.
    Делает цикл по отфильтрованным значениям habits.
    Если уведовление было отправлено ранее,
    то сверяет время уведомления с текущим временем,
    если время совпадает, то отправляет уведомление.
    Если уведомление не было отправлено ранее,
    то отправляет уведомление в указаное пользователем время.
    """
    time_max = datetime.now() + timedelta(seconds=30)
    time_min = datetime.now() - timedelta(seconds=30)
    habits = (
        Habits.objects.exclude(
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
                        + timedelta(days=habit.periodicity))
                habit.save()
        else:
            create_message(habit)
            habit.last_notification = (
                    datetime.now().date() + timedelta(days=habit.periodicity))
            habit.save()
