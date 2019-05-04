from accounts.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction


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
            Submit('submit', 'Signup', css_class='btn btn-filled btn-log margin-right'),
        )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label='', max_length=254, required=False,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name '}))
    last_name = forms.CharField(label='', max_length=254, required=False,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
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
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('last_name', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            Row(
                Column('password1', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                Column('password2', css_class='mt-10 form-group col-md-6 col-sm-12 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Signup', css_class='btn btn-filled btn-log margin-right'),
        )
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
            Submit('submit', 'Login', css_class='btn btn-filled btn-log margin-right'),  # <i class="fa fa-sign-in"></i>

        )
