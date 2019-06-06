from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DetailView

from country.forms import CountryForm
from country.models import Country


class CountryEdit(LoginRequiredMixin, UpdateView):
    model = Country
    # fields = ('description', 'photo')
    form_class = CountryForm
    template_name = 'form.html'
    success_url = reverse_lazy('country:detail')


class CountryList(ListView):
    model = Country
    context_object_name = 'country'
    template_name = 'country/list.html'


class CountryDetail(DetailView):
    model = Country
    context_object_name = 'country'
    template_name = 'country/detail.html'

