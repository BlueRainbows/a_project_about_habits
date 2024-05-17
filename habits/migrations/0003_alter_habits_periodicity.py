# Generated by Django 5.0.6 on 2024-05-13 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habits',
            name='periodicity',
            field=models.CharField(choices=[('Каждый день', 'Every day'), ('Раз в несколько дней', 'Every few days'), ('Раз в неделю', 'Once a week')], default='Каждый день', max_length=50, verbose_name='Периодичность'),
        ),
    ]
