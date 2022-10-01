from django_filters import DateTimeFilter, NumberFilter, AllValuesFilter
from rest_framework import filters

from .models import Competition

class IsOwnerFilterBackend(filters.BaseFilterBackend):
    """
    Фильтр, который позволяет пользователям видеть только свои собственные объекты.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class CompetitionFilter(filters.FilterSet):
    from_achievement_date = DateTimeFilter(
        name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = DateTimeFilter(
        name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = NumberFilter(
        name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = NumberFilter(
        name='distance_in_feet', lookup_expr='lte')
    drone_name = AllValuesFilter(
        name='drone__name')
    pilot_name = AllValuesFilter(
        name='pilot__name')

    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            'drone_name',
            'pilot_name',
        )