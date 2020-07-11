from django_filters import rest_framework as filters

from api.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category=filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    name=filters.CharFilter(field_name='name', lookup_expr='startswith')
    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year',]