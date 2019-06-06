from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from category.models import Category
from location.forms import LocationForm
from location.models import Location


class LocationCreate(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'form.html'


class LocationEdit(LoginRequiredMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template_name = 'form.html'


class LocationDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('location_list')
    template_name = 'delete.html'


class LocationList(ListView):
    model = Location
    context_object_name = 'location'
    template_name = 'location/list.html'


class LocationDetail(DetailView):
    model = Location
    context_object_name = 'location'
    template_name = 'location/detail.html'

