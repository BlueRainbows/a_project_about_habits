from django.db import models

NULLABLE = {'blank': True, 'null': True}

PERIOD_CHOICES = (
    ('Каждый день', 'Every day'),
    ('Раз в несколько дней', 'Every few days'),
    ('Раз в неделю', 'Once a week'),
)


class Habits(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        ** NULLABLE
        )
    place = models.CharField(max_length=150, verbose_name='Место', **NULLABLE)
    time = models.TimeField(verbose_name='Время', **NULLABLE)
    action = models.TextField(verbose_name='Действие')
    periodicity = models.CharField(
        max_length=50, verbose_name='Периодичность',
        choices=PERIOD_CHOICES, default='Каждый день'
    )
    time_to_complete = models.TimeField(
        verbose_name='Время на выполнение',
        **NULLABLE
    )
    award = models.TextField(verbose_name='Награда', **NULLABLE)
    publish = models.BooleanField(verbose_name='Опубликовать', default=False)
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
        return f'Я буду {self.action} в {self.time} в {self.place}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
