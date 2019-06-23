from builtins import super

import django_filters
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.regex_helper import Group
from django.views.generic import TemplateView

from accounts import forms
from accounts.models import User
from category.models import Category
from company.models import Company
from job.models import Job
from reviews.models import Review


class HomeIndex(TemplateView):
    model = None
    context_object_name = 'home'
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeIndex, self).get_context_data(**kwargs)
        context['company'] = Company.objects.all()
        context['job'] = Job.objects.all()
        context['category'] = Category.objects.all()
        context['reviews'] = Review.objects.all()

        return context


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'groups']


class Dashboard(LoginRequiredMixin,  TemplateView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.all()[:5]
        context['job'] = Job.objects.all()[:5]
        context['category'] = Category.objects.all()[:5]
        context['reviews'] = Review.objects.all()[:5]

        return context
