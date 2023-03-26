import calendar
import time

from celery import shared_task
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from calculation.models import MonthResult
from salary_calculation.tasks import test_task, send_result_email_task
from working_calendar.models import Month, Day, KindOfDay, Year


def calc(queryset):
    sum_of_hours = 0
    for i in queryset:
        sum_of_hours += i.working_hours
    return sum_of_hours


@receiver(post_save, sender=Year)
def create_month(instance, **kwargs):
    months = Month.objects.all().filter(year=instance)
    if len(months) == 0:
        months_names = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
                        'Октябрь', 'Ноябрь', 'Декабрь']
        for i in range(12):
            Month(
                number=(i + 1),
                name=months_names[i],
                year=instance,
            ).save()


@receiver(post_init, sender=Day)
def set_date_to_model(instance, **kwargs):
    instance.date_of_day = instance.get_date()


@receiver(post_init, sender=Day)
def set_kind_of_day(instance, **kwargs):
    if instance.kind_of_day is None:
        weekend = KindOfDay.objects.all().filter(name='Выходной')[0]
        working_day = KindOfDay.objects.all().filter(name='Рабочий')[0]
        day_of_week = calendar.weekday(instance.month.year.number, instance.month.number, instance.number)
        if day_of_week == 5 or day_of_week == 6:
            instance.kind_of_day = weekend
        else:
            instance.kind_of_day = working_day


# Нужно пересмотреть логику
@receiver(post_init, sender=Day)
def update_hours(instance, **kwargs):
    # if instance.working_hours == 0 or 8 or 11:
        if instance.city.is_business_trip:
            instance.working_hours = 11
        elif instance.kind_of_day.is_working_day:
            instance.working_hours = 8
        elif not instance.kind_of_day.is_working_day:
            instance.working_hours = 0
            # instance.city = None
        # print(type(instance.city))


@receiver(post_save, sender=Month)
def create_days(instance, **kwargs):
    days = Day.objects.all().filter(month=instance)
    if len(days) == 0:
        number_of_days_in_month = calendar.monthrange(instance.year.number, instance.number)[1]
        for i in range(number_of_days_in_month):
            Day(
                number=(i + 1),
                month=instance,
                kind_of_day=None,
                city_id=1
            ).save()


@receiver(post_save, sender=Month)
def create_month_result(instance, **kwargs):
    month = MonthResult.objects.all().filter(month=instance)
    list_of_days = Day.objects.all().filter(month=instance)
    if len(month) == 0:
        MonthResult(
            month=instance,
            hours=calc(list_of_days)
        ).save()


@receiver(post_save, sender=Day)
def calculate_hours(instance, **kwargs):
    number_of_days_in_month = calendar.monthrange(instance.month.year.number, instance.month.number)[1]
    month = MonthResult.objects.all().filter(month=instance.month).first()
    list_of_days = Day.objects.all().filter(month=instance.month)
    hours = 0
    if len(list_of_days) == number_of_days_in_month and month:
        for day in list_of_days:
            hours = hours + day.working_hours
        month.hours = hours
        month.save()


@receiver(post_init, sender=MonthResult)
def set_income_to_model(instance, **kwargs):
    if instance.salary:
        instance.income_per_hour = instance.get_income()


@receiver(post_init, sender=MonthResult)
def set_expected_salary(instance, **kwargs):
    months = Month.objects.order_by('id').filter(monthresult__lt=instance)
    i = len(months)
    if i >= 3:
        months = months[(i - 3):]
        sum_of_income_per_hour = 0
        try:
            for month in months:
                sum_of_income_per_hour += month.monthresult.income_per_hour
            expected_income_per_hour = round((sum_of_income_per_hour / 3), 2)
            expected_salary = expected_income_per_hour * instance.hours
            instance.expected_salary = expected_salary
        except:
            pass
