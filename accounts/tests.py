from django.test import TestCase
from django.urls import resolve, reverse

from accounts.models import User
from .forms import SignUpForm, LoginForm, EmployerSignUpForm
from .views import SignUpView, NormalSignUpView, EmployerSignUpView, UserLogin


class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/')
        self.assertEquals(view.func.view_class, SignUpView)


class NormalSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:normal_user_signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/normal_user/')
        self.assertEquals(view.func.view_class, NormalSignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)


class EmployerSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:employer_signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/signup/employer/')
        self.assertEquals(view.func.view_class, EmployerSignUpView)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, EmployerSignUpForm)


# class SuccessfulSignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         data = {
#             'username': 'john',
#             'password1': 'abcdef123456',
#             'password2': 'abcdef123456'
#         }
#         self.response = self.client.post(url, data)
#         self.home_url = reverse('category:list')
#
#     def test_redirection(self):
#         '''
#         A valid form submission should redirect the user to the home page
#         '''
#         self.assertRedirects(self.response, self.home_url)
#
#     def test_user_creation(self):
#         self.assertTrue(User.objects.exists())
#
#     def test_user_authentication(self):
#         '''
#         Create a new request to an arbitrary page.
#         The resulting response should now have a `user` to its context,
#         after a successful sign up.
#         '''
#         response = self.client.get(self.home_url)
#         user = response.context.get('user')
#         self.assertTrue(user.is_authenticated)
#
#
# class InvalidSignUpTests(TestCase):
#     def setUp(self):
#         url = reverse('accounts:signup')
#         self.response = self.client.post(url, {})  # submit an empty dictionary
#
#     def test_signup_status_code(self):
#         '''
#         An invalid form submission should return to the same page
#         '''
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_form_errors(self):
#         form = self.response.context.get('form')
#         self.assertTrue(form.errors)
#
#     def test_dont_create_user(self):
#         self.assertFalse(User.objects.exists())


class LoginUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:login')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve('/accounts/login/')
        self.assertEquals(view.func.view_class, UserLogin)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, LoginForm)
