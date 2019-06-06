from builtins import super

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.core.checks import messages
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from hitcount.views import HitCountDetailView

from accounts.decorators import UserRequiredMixin
from category.models import Category
from company.models import Company, CompanyImage, OpeningHours, ClosingRules
# Category views
from jobcorner import settings
from location.models import Location
from reviews.forms import ReviewForm
from .filters import CompanyFilter
from .forms import CompanyForm, OpeningHoursForm, CompanyFilterForm


def company_list_view(request):
    company_list = Company.objects.all()
    company_filter = CompanyFilter(request.GET, queryset=company_list)
    form = CompanyFilterForm(data=request.GET)

    facets = {
        "selected": {},
        "catego": {
            "category": Category.objects.all(),
            "location": Location.objects.all(),
        },
    }
    if form.is_valid():
        category = form.cleaned_data["category"]
        if category:
            facets["selected"]["category"] = category
        company_list = company_list.filter(category=category).distinct()
        location = form.cleaned_data["location"]
        if location:
            facets["selected"]["location"] = location
        company_list = company_list.filter(location=location).distinct()

    if settings.DEBUG:
        from pprint import pprint
        pprint(facets)

    context = {
        "form": form,
        "facets": facets,
        "object_list": company_list,
        'filter': company_filter,
    }

    return render(request, 'company/list.html', context)


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


class CompanyDetail(HitCountDetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'company'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['meta'] = self.get_object().as_meta(self.request)
        context['company_image'] = CompanyImage.objects.filter(company=self.get_object())
        context['open_hours'] = OpeningHours.objects.filter(company=self.get_object())
        context['closing_rules'] = ClosingRules.objects.filter(company=self.get_object())
        context['form'] = ReviewForm()
        context['related'] = self.object.tags.similar_objects()[:4]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


#
# class OpeningHourCreate(LoginRequiredMixin, ModelFormSetView):
#     model = OpeningHours
#     form_class = OpeningHoursForm
#     # formset_class = OpeningHoursFormset
#     template_name = 'company/formset.html'
#     flocationy_kwargs = {'can_order': False, 'can_delete': False}
#     # formset_kwargs = {'auto_id': 'my_id_%s'}
#
#
#     def form_valid(self, form):
#         form.instance.company = get_object_or_404(Company, slug=self.kwargs['slug'])
#         form.save()
#         return super().form_valid(form)
#
#     def form_invalid(self, form):
#         """
#         If the form is invalid, re-render the context data with the
#         data-filled form and errors.
#         """
#         print('the is an error in your form')
#         messages.warning(self.request, 'There was an error in this form')
#         return self.render_to_response(self.get_context_data(form=form))
#


class OpeningHourCreate(LoginRequiredMixin, CreateView):
    model = OpeningHours
    form_class = OpeningHoursForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.company = get_object_or_404(Company, slug=self.kwargs['slug'])
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

# follow(request.user)
# unfollow(request.user)
# followers(request.user) # returns a list of Users who follow request.user
# following(request.user) # returns a list of locations who request.user is following
