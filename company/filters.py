import django_filters
from django import forms

from .models import Company


class CompanyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Company Name'}))
    description = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                            widget=forms.TextInput(attrs={'placeholder': 'description'}))

    class Meta:
        model = Company
        fields = ['name', 'description']
