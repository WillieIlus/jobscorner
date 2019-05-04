from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

# from src.accounts.models import Profile
# from resume.views import ProfileCreateView
from .views import NormalSignUpView, EmployerSignUpView, SignUpView, UserLogin, UserUpdateView, validate_email, \
    validate_username

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signup/normal_user/', NormalSignUpView.as_view(), name='normal_user_signup'),
    path('signup/employer/', EmployerSignUpView.as_view(), name='employer_signup'),
    path('ajax/validate_username/', validate_username, name='validate_username'),
    path('ajax/validate_username/', validate_email, name='validate_email'),
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
    path('settings/account_edit/', UserUpdateView.as_view(), name='account_edit'),
    # path('users/', UserList.as_view(), name='users'),
    # path('<slug>/', Profile.as_view(), name='account'),
    # path('create/', ProfileCreateView.as_view(), name='create_profile'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html',
                                                                     success_url=reverse_lazy(
                                                                         'accounts:password_change_done')),
         name='password_change'),
    path('settings/password/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

]
