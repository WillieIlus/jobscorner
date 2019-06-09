from accounts.decorators import normal_user_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, CreateView
from django_xhtml2pdf.utils import render_to_pdf_response

from .forms import ProfileForm, SkillForm, ExperienceForm, EducationForm
from .models import Profile, Skill, Experience, Education


class ProfileList(ListView):
    queryset = Profile.published.all()
    context_object_name = 'profile'
    template_name = 'resume/list.html'
    paginate_by = 6


class ProfileDetail(DetailView):
    queryset = Profile.published.all()
    context_object_name = 'profile'
    template_name = 'resume/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skill_list'] = Skill.objects.filter(profile=self.get_object())
        context['education_list'] = Education.objects.filter(profile=self.get_object())
        context['experience_list'] = Experience.objects.filter(profile=self.get_object())
        return context


@method_decorator([login_required, normal_user_required], name='dispatch')
class ProfileDelete(DeleteView):
    model = Profile
    success_url = reverse_lazy('profile:list')
    context_object_name = 'profile'
    template_name = 'resume/delete.html'


@method_decorator([login_required, normal_user_required], name='dispatch')
class ProfileCreate(CreateView):
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.profile = get_object_or_404(Profile, slug=self.kwargs['slug'])
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


class SkillsCreate(ProfileCreate):
    model = Skill
    form_class = SkillForm


class ExperienceCreate(ProfileCreate):
    model = Experience
    form_class = ExperienceForm


class EducationCreate(ProfileCreate):
    model = Education
    form_class = EducationForm

@method_decorator([login_required, normal_user_required], name='dispatch')
class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        print('there is an error in your form')
        messages.warning(self.request, 'There was an error in this form')
        return self.render_to_response(self.get_context_data(form=form))


class PdfResponseMixin(object, ):
    pdf_name = "output"

    def get_pdf_name(self):
        return self.pdf_name

    def render_to_response(self, context, **response_kwargs):
        context = self.get_context_data()
        template = self.get_template_names()[0]
        resp = HttpResponse(content_type='application/pdf')
        resp['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(self.get_pdf_name())
        result = render_to_pdf_response(template, context=context)
        return result


class CVPdfDetailView(PdfResponseMixin, DetailView):
    context_object_name = 'profile'
    # slug_field = "username"
    model = Profile
    template_name = 'resume/cv/cv_pdf.html'
