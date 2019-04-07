from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from accounts import views as accounts_views
from .views import NormalSignUpView, EmployerSignUpView, SignUpView, UserLogin, ResumeEdit

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/normal_user/', NormalSignUpView.as_view(), name='normal_user_signup'),
    path('signup/employer/', EmployerSignUpView.as_view(), name='employer_signup'),
    path('ajax/validate_username/', accounts_views.validate_username, name='validate_username'),
    path('ajax/validate_username/', accounts_views.validate_email, name='validate_email'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',
                                                        email_template_name='accounts/password_reset_email.html',
                                                        subject_template_name='accounts/password_reset_subject.txt'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    # path('settings/account/', accounts_views.UserDetail.as_view(), name='my_account'),
    path('settings/account_edit/', accounts_views.UserUpdateView.as_view(), name='account_edit'),
    path('users/', accounts_views.UserList.as_view(), name='users'),
    path('<slug>/account/', accounts_views.UserDetail.as_view(), name='account'),
    path('create/', accounts_views.ResumeCreate.as_view(), name='create_resume'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                                     success_url=reverse_lazy(
                                                                         'accounts:password_change_done')),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    # Resume and Profile
    path('<slug>/resume/', accounts_views.ProfileCreate.as_view(), name='add_profile'),
    path('<slug>/resume/edit/',  accounts_views.ProfileEdit.as_view(), name='edit_profile'),
    path('<slug>/education/',  accounts_views.EducationCreate.as_view(), name='add_education'),
    path('<slug>/skills/',  accounts_views.SkillsCreate.as_view(), name='add_skills'),
    path('<slug>/experience/',  accounts_views.ExperienceCreate.as_view(), name='add_experience'),
    path('like/', accounts_views.profile_like, name='like'),
    # path('<slug>/resume/edit/', ResumeEdit.as_view(), name='edit_resume'),
    # path('<slug>/resume/edit/', ResumeEdit.as_view(), name='edit_resume'),
    # path('<slug>/resume/edit/', ResumeEdit.as_view(), name='edit_resume'),
    # path('<slug>/resume/edit/', ResumeEdit.as_view(), name='edit_resume'),

]
