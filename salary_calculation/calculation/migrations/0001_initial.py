# Generated by Django 4.1.4 on 2023-02-26 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('working_calendar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthResult',
            fields=[
                ('month', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='working_calendar.month')),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Salary')),
                ('hours', models.IntegerField(blank=True, null=True, verbose_name='Hours')),
                ('income_per_hour', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Income per hour')),
                ('expected_salary', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name='Expected salary')),
            ],
            options={
                'verbose_name': 'Результаты месяца',
                'verbose_name_plural': 'Результаты месяцев',
            },
        ),
    ]
