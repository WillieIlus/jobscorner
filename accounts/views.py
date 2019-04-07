from accounts.forms import SignUpForm, EmployerSignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView

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


def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'This email is already taken.'
    return JsonResponse(data)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


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

    def get_object(self):
        return self.request.user


class UserList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/list.html'
    paginate_by = 20


class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/detail.html'
    context_object_name = 'user'
    slug_field = 'username'


class ResumeCreate(LoginRequiredMixin, CreateView):
    template_name = 'accounts/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
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

    def get_success_url(self):
        user = self.request.user
        # user = get_object_or_404(User)
        return reverse('accounts:account', kwargs={"slug": user.slug})
        # return HttpResponseRedirect(reverse('accounts:account', args=(user.slug,)))


class SkillsCreate(ResumeCreate):
    model = Skill
    fields = ['name', 'description', 'level', 'tags']


class ExperienceCreate(ResumeCreate):
    model = Experience
    fields = ['role', 'company', 'company_url', 'start_date', 'completion_date', 'description', 'is_current']


class EducationCreate(ResumeCreate):
    model = Education
    fields = ['school', 'school_url', 'major', 'result', 'start_date', 'completion_date', 'summary', 'is_current']


class RefereeCreate(ResumeCreate):
    model = Referee
    fields = ['full_name', 'position', 'company', 'phone', 'email']


class ProfileCreate(LoginRequiredMixin, CreateView):
    model = NormalUser
    fields = ['bio', 'location', 'birth_date', 'thumbnail', 'phone', 'website', 'facebook', 'instagram', 'twitter',
              'linkedin', 'google', 'pinterest']
    template_name = 'accounts/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
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

    def get_success_url(self):
        return reverse('accounts:account', kwargs={'slug': self.slug})


class ResumeEdit(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


class ProfileEdit(ResumeEdit):
    model = NormalUser
    fields = ['bio', 'location', 'birth_date', 'thumbnail', 'phone', 'website', 'facebook', 'instagram', 'twitter',
              'linkedin', 'google', 'pinterest']

@login_required
@require_POST
# def image_like(request):
#     image_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if image_id and action:
#         try:
#         image = Image.objects.get(id=image_id)
#         if action == 'like':
#         image.users_like.add(request.user)
#         else:
#         image.users_like.remove(request.user)
#         return JsonResponse({'status':'ok'})
#         except:
#         pass
#     return JsonResponse({'status':'ko'})

def profile_like(request):
    profile = get_object_or_404(NormalUser, user=request.POST.get('user_id'))
    profile.like.add(request.user)
    return HttpResponseRedirect(profile.get_absolute_url())



# def profile_like(request):
#     profile_id = request.POST.get('id')
#     action = request.POST.get('action')
#     if profile_id and action:
#         try:
#             profile = NormalUser.objects.get(id=profile_id)
#             if action == 'like':
#                 profile.users_like.add(request.user)
#             else:
#                 profile.users_like.remove(request.user)
#             return JsonResponse({'status':'ok'})
#         except:
#             pass
#     return JsonResponse({'status':'ko'})