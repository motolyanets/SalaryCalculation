from collections import OrderedDict

from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer
from .models import Day, Month, Year, City, KindOfDay
from .services import calc


class DaySerializer(ModelSerializer):
    month = IntegerField(source='month.id')

    class Meta:
        model = Day
        fields = '__all__'


class MonthSerializer(ModelSerializer):
    year = IntegerField(source='year.number')
    # hours = IntegerField()

    class Meta:
        model = Month
        # fields = ("id", "number", "name", "year", "salary")
        fields = '__all__'


    # def to_representation(self, instance):
    #     object = MonthSerializer(Month.objects.all()[0])
    #
    #     result = super().to_representation(instance)
    #     result["hours"] = object.calculate_hours()
    #     return result




class YearSerializer(ModelSerializer):


    class Meta:
        model = Year
        fields = ("id", "content", "createdAt", "executor")


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "content", "createdAt", "executor")


class KindOfDaySerializer(ModelSerializer):
    class Meta:
        model = KindOfDay
        fields = ("id", "content", "createdAt", "executor")



