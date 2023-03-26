from django.contrib import admin
from .models import Day, Month, Year, City, KindOfDay, User


class DayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Day._meta.fields]

    class Meta:
        model = Day


class MonthAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Month._meta.fields]

    class Meta:
        model = Month


class YearAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Year._meta.fields]

    class Meta:
        model = Year


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]

    class Meta:
        model = City


class KindOfDayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in KindOfDay._meta.fields]

    class Meta:
        model = KindOfDay

admin.site.register(Day, DayAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Year, YearAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(KindOfDay, KindOfDayAdmin)
admin.site.register(User)
