# Generated by Django 5.0.6 on 2024-05-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0003_alter_habits_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habits',
            name='sign_pleasant_habit',
            field=models.BooleanField(default=False, verbose_name='Признак приятной привычки'),
        ),
    ]
