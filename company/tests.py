from django.test import TestCase
from django.urls import reverse, resolve

from accounts.models import User
from category.models import Category
from company.models import Company
from company.views import CompanyList


class CompanyListTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='john',
            email='john@gmail.com',
            password='1234john'
        )
        category = Category.objects.create(
            name='Graphic Design',
            description='The quick brown'
        )
        self.company = Company.objects.create(
            name='brandlogic',
            description='lorem ipsum',
            user=user,
            category=category,
            website='www.brandlogic.com',
            email='brand@logic.com'
        )

        url = reverse('company:list')
        self.response = self.client.get(url)

    def test_list_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_list_url_resolves_view(self):
        view = resolve('/company/')
        self.assertEquals(view.func.view_class, CompanyList)

    def test_list_view_contains_detail_links(self):
        company_detail_url = reverse('company:detail', kwargs={'slug': 'brandlogic'})
        response = self.client.get(company_detail_url)
        self.assertContains(response, company_detail_url)

    def test_list_view_contains_add_links(self):
        company_new_url = reverse('company:add')
        response = self.client.get(company_new_url)
        self.assertContains(response, company_new_url)


class CompanyDetailTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='john',
            email='john@gmail.com',
            password='1234john'
        )
        category = Category.objects.create(
            name='Graphic Design',
            description='The quick brown'
        )
        self.company = Company.objects.create(
            name='brandlogic',
            description='lorem ipsum',
            user=user,
            category=category,
            website='www.brandlogic.com',
            email='brand@logic.com'
        )

    def test_company_view_success_status_code(self):
        url = reverse('company:detail', kwargs={'slug': 'brandlogic'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_company_view_not_found_status_code(self):
        url = reverse('company:detail', kwargs={'slug': 'kenya'})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    # def test_company_url_resolves_company_view(self):
    #     view = resolve('/company/brandlogic/')
    #     self.assertEquals(view.func.view_class, CompanyDetail)

    def test_company_view_contains_link_back_to_company_list_view(self):
        company_list_url = reverse('company:list')
        response = self.client.get(company_list_url)
        self.assertContains(response, company_list_url)


#

class CompanyUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            email='john@gmail.com',
            password='1234john'
        )
        self.category = Category.objects.create(
            name='Graphic Design',
            description='The quick brown'
        )
        Company.objects.create(
            name='brandlogic',
            description='lorem ipsum',
            user=self.user,
            category=self.category,
            website='www.brandlogic.com',
            email='brand@logic.com'
        )
        self.url = reverse('company:update', kwargs={'slug': 'brandlogic'})


class LoginRequiredCompanyUpdateViewTests(CompanyUpdateViewTestCase):
    def test_redirection(self):
        '''
        Test if only logged in users can edit the posts
        '''
        login_url = reverse('accounts:login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
#
#
# class CompanyUpdateViewTests(CompanyUpdateViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.get(self.url)
#
#     def test_status_code(self):
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_view_class(self):
#         view = resolve('/company/kenya/edit/')
#         self.assertEquals(view.func.view_class, CompanyEdit)
#
#     def test_csrf(self):
#         self.assertContains(self.response, 'csrfmiddlewaretoken')
#
#     def test_contains_form(self):
#         form = self.response.context.get('form')
#         self.assertIsInstance(form, ModelForm)
#
#
# class SuccessfulCompanyUpdateViewTests(CompanyUpdateViewTestCase):
#     def setUp(self):
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, {'message': 'edited message'})
#
#     def test_redirection(self):
#         '''
#         A valid form submission should redirect the user
#         '''
#         company_list_url = reverse('company:detail', kwargs={'slug': 'kenya'})
#         self.assertRedirects(self.response, company_list_url)
#
#     def test_company_changed(self):
#         self.company.refresh_from_db()
#         self.assertEquals(self.company.description, 'The quick brown fox jumps over the lazy dog')
#
#
# class InvalidCategoryUpdateViewTests(CompanyUpdateViewTestCase):
#     def setUp(self):
#         '''
#         Submit an empty dictionary to the `reply_topic` view
#         '''
#         super().setUp()
#         self.client.login(username=self.username, password=self.password)
#         self.response = self.client.post(self.url, {})
#
#     def test_status_code(self):
#         '''
#         An invalid form submission should return to the same page
#         '''
#         self.assertEquals(self.response.status_code, 200)
#
#     def test_form_errors(self):
#         form = self.response.context.get('form')
#         self.assertTrue(form.errors)
