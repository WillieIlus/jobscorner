from builtins import super

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView, CreateView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView, ModelFormSetView, \
    FormSetView

from accounts.decorators import UserRequiredMixin
from company.models import Company, CompanyImage, OpeningHours, ClosingRules
# Category views
from reviews.forms import ReviewForm

from .filters import CompanyFilter
from .forms import CompanyForm, OpeningHoursForm, OpeningHoursFormset


def company_list_view(request):
    company_list = Company.objects.all()
    company_filter = CompanyFilter(request.GET, queryset=company_list)
    return render(request, 'company/list.html', {'filter': company_filter})


class PhotosInline(InlineFormSetFactory):
    model = CompanyImage
    # form_class = CompanyPhotoFormSet
    fields = ['img', 'alt']


class CompanyCreate(LoginRequiredMixin, CreateWithInlinesView):
    model = Company
    inlines = [PhotosInline]
    form_class = CompanyForm
    template_name = 'company/form.html'

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super(CompanyCreate, self).forms_valid(form, inlines)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = "Add your Company"


class CompanyEdit(LoginRequiredMixin, UserRequiredMixin, UpdateWithInlinesView):
    model = Company
    inlines = [PhotosInline]
    slug_url_kwarg = 'slug'
    form_class = CompanyForm
    template_name = 'company/form.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context['company'] = Company.objects.all()[:5]
    #     context['title'] = " Update Company "

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super(CompanyEdit, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()


class CompanyDelete(LoginRequiredMixin, UserRequiredMixin, DeleteView):
    model = Company
    success_url = reverse_lazy('company:list')
    template_name = 'delete.html'


class CompanyDetail(DetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'company'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_image'] = CompanyImage.objects.filter(company=self.get_object())
        context['open_hours'] = OpeningHours.objects.filter(company=self.get_object())
        context['closing_rules'] = ClosingRules.objects.filter(company=self.get_object())
        context['form'] = ReviewForm()
        context['related'] = self.object.tags.similar_objects()[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class OpeningHourCreate(LoginRequiredMixin, FormSetView):
    model = OpeningHours
    fields = ['weekday', 'from_hour', 'to_hour']
    # form_class = OpeningHoursForm
    template_name = 'company/formset.html'
    # initial = [{'type': 'home'}, {'type', 'work'}]
    factory_kwargs = {'extra': 1, 'max_num': 7,
                      'can_order': False, 'can_delete': True}

    def form_valid(self, form):
        form = form.save(Commit=False)
        form.company = get_object_or_404(Company, slug=self.kwargs['slug'])
        # form.instance.company = get_object_or_404(Company, pk=self.kwargs['company_id'])

        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        print('the is an error in your form')
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))

# class ItemFormSetView():
# model = Item
# fields = ['name', 'sku']
# template_name = 'item_formset.html'
