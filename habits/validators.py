from datetime import time

from rest_framework.serializers import ValidationError


class AwardValidator:
    """
    Валидатор исключючения одновременного выбора
    связанной привычки и указания вознаграждения.
    При одновременном заполнении вознаграждения и связанной привычки,
    возникает ошибка валидации.
    """
    def __init__(self, award, pleasant_habit):
        self.award = award
        self.pleasant_habit = pleasant_habit

    def __call__(self, value):
        get_award = dict(value).get(self.award)
        get_pleasant_habit = dict(value).get(self.pleasant_habit)
        if get_award is not None and get_pleasant_habit is not None:
            raise ValidationError(
                "Вы можете выбрать либо приятную причку, либо вознаграждение"
            )


class TimeValidator:
    """
    Валидатор проверки времени на выполнение привычки.
    Создает объект типа time
    равный максимальному времени на выполнение привычки.
    Проверяет, что время указанное пользователем не превышает 2-ух минут.
    """
    def __init__(self, time_to_complete):
        self.time_to_complete = time_to_complete

    def __call__(self, value):
        date_time = time(0, 2, 0)
        get_value = dict(value).get(self.time_to_complete)
        if get_value is not None:
            if get_value > date_time:
                raise ValidationError(
                    "Время на выполнение не может превышать 2-ух минут"
                )


class RelatedHabitValidator:
    """
    Валидатор для проверки связной привычки.
    Проверяет что в связанные привычки
    могут попадать только привычки с признаком приятной привычки (True).
    """
    def __init__(self, pleasant_habit):
        self.pleasant_habit = pleasant_habit

    def __call__(self, value):
        get_value = dict(value).get(self.pleasant_habit)
        if get_value:
            if not get_value.sign_pleasant_habit:
                raise ValidationError(
                    "Вы можете добавить только приятную привычку"
                )


class PleasantHabitValidator:
    """
    Валидатор для проверки приятной привычки.
    Проверяет что у приятной привычки
    не может быть вознаграждения или связанной привычки.
    """
    def __init__(self, sign_pleasant_habit, pleasant_habit, award):
        self.sign_pleasant_habit = sign_pleasant_habit
        self.pleasant_habit = pleasant_habit
        self.award = award

    def __call__(self, value):
        get_value = dict(value).get(self.sign_pleasant_habit)
        if get_value:
            get_pleasant_habit = dict(value).get(self.pleasant_habit)
            get_award = dict(value).get(self.award)
            if get_pleasant_habit is not None or get_award is not None:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения "
                    "или связанной привычки"
                )


class PeriodicityValidator:
    """
    Валидатор для проверки периодичности привычки.
    Проверяет что в периодичности привычки не более 7 дней.
    """
    def __init__(self, periodicity):
        self.periodicity = periodicity

    def __call__(self, value):
        get_value = dict(value).get(self.periodicity)
        if int(get_value) > 7:
            raise ValidationError(
                "Периодичность привычки не может превышать более 7 дней")
