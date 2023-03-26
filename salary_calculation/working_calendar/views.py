from rest_framework.viewsets import ModelViewSet

from .models import Day, Month
from .serializers import DaySerializer, MonthSerializer, YearSerializer, CitySerializer, KindOfDaySerializer


class DayViewSet(ModelViewSet):
    queryset = Day.objects.all().order_by('number')
    serializer_class = DaySerializer

    def filter_queryset(self, queryset):
        month_id = self.request.query_params.get('month_id')
        if month_id:
            queryset = queryset.filter(month_id=month_id)
        return queryset


class MonthViewSet(ModelViewSet):
    queryset = Month.objects.all().order_by('number')
    serializer_class = MonthSerializer

    def filter_queryset(self, queryset):
        month_number = self.request.query_params.get('month_number')
        if month_number:
            queryset = queryset.filter(number=month_number)
        return queryset







