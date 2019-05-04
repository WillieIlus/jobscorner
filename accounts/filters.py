import django_filters
from django import forms

from .models import Profile, User


class ProfileFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='', required=False,
                                      widget=forms.TextInput(attrs={'placeholder': 'title'}))
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), lookup_expr='icontains', label='',
                                            required=False,
                                            widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    class Meta:
        model = Profile
        fields = ['title', 'user']
