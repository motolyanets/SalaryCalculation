from django.contrib import admin
from .models import MonthResult


class MonthResultAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MonthResult._meta.fields]

    class Meta:
        model = MonthResult

admin.site.register(MonthResult, MonthResultAdmin)
