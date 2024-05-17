from rest_framework import serializers

from habits.models import Habits
from habits.validators import (AwardValidator, TimeValidator,
                               RelatedHabitValidator,
                               PleasantHabitValidator,
                               PeriodicityValidator)


class HabitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habits
        fields = '__all__'
        validators = [
            AwardValidator(award='award',
                           pleasant_habit='pleasant_habit'),

            TimeValidator(time_to_complete='time_to_complete'),

            RelatedHabitValidator(pleasant_habit='pleasant_habit'),

            PleasantHabitValidator(sign_pleasant_habit='sign_pleasant_habit',
                                   pleasant_habit='pleasant_habit',
                                   award='award'),

            PeriodicityValidator(periodicity='periodicity')
        ]
