from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habits(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        ** NULLABLE
        )
    place = models.CharField(
        max_length=150,
        verbose_name='Место'
    )
    time = models.TimeField(
        verbose_name='Время'
    )
    action = models.TextField(
        verbose_name='Действие'
    )
    periodicity = models.IntegerField(
        verbose_name='Периодичность',
        default=1
    )
    time_to_complete = models.TimeField(
        verbose_name='Время на выполнение',
        **NULLABLE
    )
    award = models.TextField(
        verbose_name='Награда',
        **NULLABLE
    )
    publish = models.BooleanField(
        verbose_name='Опубликовать',
        default=False
    )
    sign_pleasant_habit = models.BooleanField(
        verbose_name='Признак приятной привычки',
        default=False
    )
    pleasant_habit = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='Приятная привычка',
        **NULLABLE
    )
    last_notification = models.DateTimeField(
        verbose_name='Последнее уведомление',
        **NULLABLE
    )

    def __str__(self):
        return f'Сделать: {self.action}, в {self.time}.'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
