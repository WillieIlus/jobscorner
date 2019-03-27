from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView
from extra_views import InlineFormSetFactory, NamedFormsetsMixin, CreateWithInlinesView, UpdateWithInlinesView

from accounts.forms import SignUpForm, EmployerSignUpForm, LoginForm
from .models import User, Skill, Experience, Education, Referee, NormalUser


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class NormalSignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'normal_user'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class EmployerSignUpView(CreateView):
    model = User
    form_class = EmployerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserLogin(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Login"
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'accounts/my_account.html'
    # success_url = reverse_lazy('accounts:user_profile', kwargs=)

    def get_object(self):
        return self.request.user

    # def get_success_url(self):
    #     return reverse('accounts:user_profile', kwargs={'username': self.request.user.username})


class UserList(ListView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/list.html'
    paginate_by = 20


class UserDetail(DetailView):
    model = User
    template_name = 'accounts/detail.html'
    context_object_name = 'user'
    slug_field = 'username'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['skill'] = Skill.objects.filter(company=self.get_object())
    #     context['experience'] = Experience.objects.filter(company=self.get_object())
    #     context['education'] = Education.objects.filter(company=self.get_object())
    #     context['referee'] = Referee.objects.filter(company=self.get_object())
    #     return context


class SkillsView(InlineFormSetFactory):
    model = Skill
    fields = ['name', 'description', 'level', 'tags']


class ExperienceView(InlineFormSetFactory):
    model = Experience
    fields = ['role', 'company', 'company_url', 'start_date', 'completion_date', 'description', 'is_current']


class EducationVew(InlineFormSetFactory):
    model = Education
    fields = ['school', 'school_url', 'major', 'result', 'start_date', 'completion_date', 'summary', 'is_current']


class RefereeView(InlineFormSetFactory):
    model = Referee
    fields = ['full_name', 'position', 'company', 'phone', 'email']


class ResumeCreate(NamedFormsetsMixin, CreateWithInlinesView):
    model = NormalUser
    inlines = [SkillsView, ExperienceView, EducationVew, RefereeView]
    inlines_names = ['Skills', 'Experience', 'Education', 'Referees']
    fields = ['bio', 'location', 'birth_date', 'thumbnail', 'phone', 'website', 'facebook', 'instagram',
              'twitter', 'linkedin', 'google', 'pinterest']
    template_name = 'accounts/form.html'

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super(ResumeCreate, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()


class ResumeEdit(NamedFormsetsMixin, UpdateWithInlinesView):
    model = NormalUser
    inlines = [SkillsView, ExperienceView, EducationVew, RefereeView]
    inlines_names = ['Skills', 'Experience', 'Education', 'Referees']
    fields = ['title', 'resume', 'objective', 'hobbies', 'users_like']
    template_name = 'accounts/form.html'

    def forms_valid(self, form, inlines):
        form.instance.user = self.request.user
        return super(ResumeEdit, self).forms_valid(form, inlines)

    def get_success_url(self):
        return self.object.get_absolute_url()
