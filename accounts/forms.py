from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction

from accounts.models import User


class SignUp(UserCreationForm):
    username = forms.CharField(label='', max_length=254, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}))
    email = forms.CharField(label='', max_length=254, required=True,
                            widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='', max_length=254, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='', max_length=254, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Signup'),
        )


class SignUpForm(SignUp):
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_normal_user = True
        user.save()
        return user


class EmployerSignUpForm(SignUp):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_employer = True
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='', max_length=254, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(label='', max_length=254, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Login'),
        )
