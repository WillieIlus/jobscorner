from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from category.forms import CategoryForm
from category.models import Category


class CategoryList(ListView):
    model = Category
    context_object_name = "category"
    template_name = 'category/list.html'


class CategoryDetail(DetailView):
    model = Category
    context_object_name = "category"
    template_name = 'category/detail.html'


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Add Category "
        return context


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = " Update Category "
        return context


class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category:list')
    template_name = 'delete.html'
