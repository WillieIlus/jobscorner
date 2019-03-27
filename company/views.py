from builtins import super

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, DeleteView
from extra_views import CreateWithInlinesView, InlineFormSetFactory, UpdateWithInlinesView

# from SRC.reviews.forms import ReviewForm
from accounts.decorators import UserRequiredMixin
from company.models import Company, CompanyImage
# Category views
from reviews.forms import ReviewForm
from .forms import CompanyForm


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


class CompanyList(ListView):
    model = Company
    context_object_name = 'company'
    template_name = 'company/list.html'
    paginate_by = 2


class CompanyDetail(DetailView):
    model = Company
    template_name = 'company/detail.html'
    context_object_name = 'company'
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company_image'] = CompanyImage.objects.filter(company=self.get_object())
        # context['review'] = Review.objects.all().order_by('-pub_date')
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
