import django_filters
from django import forms

from .models import Job


class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Job Title'}))
    salary = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                     widget=forms.TextInput(attrs={'placeholder': 'Salary'}))
    description = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                            widget=forms.TextInput(attrs={'placeholder': 'Description'}))

    class Meta:
        model = Job
        fields = ['title', 'salary', 'description']
