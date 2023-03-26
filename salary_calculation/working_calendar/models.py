from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from datetime import date


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("The email must be set")
        if not password:
            raise ValueError("The password must be set")
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField("Email", unique=True, max_length=256, blank=False)
    name = models.CharField(max_length=40, db_index=True, default='A', blank=False)
    surname = models.CharField(max_length=40, db_index=True, default='M', blank=False)
    is_staff = models.BooleanField("Is staff", default=False)
    is_active = models.BooleanField("Is active", default=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        app_label = "working_calendar"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.pk}: {self.email}"

    def has_module_perms(self, app_label):
        return self.is_staff and self.is_active

    def has_perm(self, perm_list, obj=None):
        return self.is_staff and self.is_active


class Day(models.Model):
    date_of_day = models.DateField("Date", unique=True, primary_key=True, blank=False)
    number = models.IntegerField("Number", blank=False)
    month = models.ForeignKey('Month', on_delete=models.CASCADE, null=True)
    kind_of_day = models.ForeignKey('KindOfDay', on_delete=models.PROTECT, null=True)
    city = models.ForeignKey('City', on_delete=models.PROTECT, blank=True, null=True)
    working_hours = models.IntegerField("Hours", blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'Дни'

    def __str__(self):
        return str(self.date_of_day)

    def get_date(self):
        date_of_day = date(self.month.year.number, self.month.number, self.number)
        return date_of_day


class Month(models.Model):
    number = models.IntegerField("Month number", blank=False)
    name = models.TextField("Month name", max_length=20, blank=False, null=True)
    year = models.ForeignKey('Year', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Месяц'
        verbose_name_plural = 'Месяца'

    def __str__(self):
        return f'{self.name} {self.year}'


class Year(models.Model):
    number = models.IntegerField("Year number", blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, default=1)

    class Meta:
        verbose_name = 'Год'
        verbose_name_plural = 'Года'

    def __str__(self):
        return str(self.number)


class City(models.Model):
    name = models.TextField("City", unique=True, max_length=20, blank=False)
    is_business_trip = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self):
        return self.name


class KindOfDay(models.Model):
    name = models.TextField("KindOfDay", unique=True, max_length=20, blank=False)
    is_working_day = models.BooleanField(default=True)
    is_sick_leave = models.BooleanField(default=False)
    is_vacation = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Вид дня'
        verbose_name_plural = 'Виды дня'

    def __str__(self):
        return self.name
