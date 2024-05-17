# Generated by Django 5.0.6 on 2024-05-16 16:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_alter_habits_sign_pleasant_habit'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='habits',
            name='last_notification',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Последнее уведомление'),
        ),
        migrations.AlterField(
            model_name='habits',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
