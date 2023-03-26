from django.db import models
from working_calendar.models import Month


class MonthResult(models.Model):
    month = models.OneToOneField(Month, on_delete=models.CASCADE, primary_key=True)
    salary = models.DecimalField("Salary", max_digits=6, decimal_places=2, blank=True, null=True)
    hours = models.IntegerField("Hours", blank=True, null=True)
    income_per_hour = models.DecimalField("Income per hour", max_digits=4, decimal_places=2, blank=True, null=True)
    expected_salary = models.DecimalField("Expected salary", max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'Результаты месяца'
        verbose_name_plural = 'Результаты месяцев'

    def __str__(self):
        return f'{self.month}'

    def get_income(self):
        income_per_hour = self.salary / self.hours
        return round(income_per_hour, 2)

